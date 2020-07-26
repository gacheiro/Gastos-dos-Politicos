from datetime import datetime

import click
import sqlalchemy

from gastos_politicos.ext.cache import cache
from gastos_politicos.models import db, Politico, Reembolso
from .dados_abertos import deputados, despesas


def create_db():
    """Cria as tabelas do banco de dados."""
    db.create_all()


def drop_db():
    """Deleta as tabelas do banco de dados."""
    db.drop_all()


def clear_cache():
    """Limpa todos os dados da cache."""
    cache.clear()


def obter_deputados(fetch=deputados):
    """Popula o banco de dados com os deputados da legislação atual."""
    dados = fetch()
    for dep in dados:
        d = Politico(
            id=dep["id"],
            nome=dep["nome"],
            email=dep["email"],
            partido=dep["siglaPartido"],
            uf=dep["siglaUf"],
            legislatura=dep["idLegislatura"],
            url_foto=dep["urlFoto"],
        )
        _commit(d)


@click.option("--id", help="id do politico.")
@click.option("--mes", help="mês das despesas.")
@click.option("--ano", help="ano das despesas.")
def obter_despesas(id, ano, mes, fetch=despesas):
    """Popula o banco de dados com as últimas despesas dos deputados."""
    print(f"obter-despesas --id {id} --ano {ano} --mes {mes}")
    if id:
        _obter_despesas(id, mes, ano, fetch=despesas)
    else:
        query = Politico.query.order_by(Politico.nome)
        for i, p in enumerate(query.all(), 1):
            print(f"{i} - [{p.id}] Obtendo as despesas de {p.nome}.")
            _obter_despesas(p.id, mes, ano, fetch=despesas)
    print("Atualização completa.")


def _obter_despesas(id, mes, ano, fetch=despesas):
    dados = fetch(id, mes=mes, ano=ano)
    for desp in dados:
        # Algumas despesas têm dataDocumento=null, apenas ignore por enquanto
        # TODO: reconstruir a data da despesa com o ano e o mês
        if desp["dataDocumento"] is None:
            print(f"Ignorando despesa sem data R$ {desp['valorLiquido']}")
            continue
        d = Reembolso(
            politico_id=id,
            cod_documento=desp["codDocumento"],
            num_documento=desp["numDocumento"],
            tipo_documento=desp["tipoDocumento"],
            tipo=desp["tipoDespesa"],
            ano=desp["ano"],
            mes=desp["mes"],
            data=datetime.strptime(desp["dataDocumento"], "%Y-%m-%d"),
            valor=desp["valorDocumento"],
            valor_liquido=desp["valorLiquido"],
            url_documento=desp["urlDocumento"],
            nome_fornecedor=desp["nomeFornecedor"],
            id_fornecedor=desp["cnpjCpfFornecedor"],
        )
        _commit(d)


def _commit(obj, ignore=False):
    """Insere o obj no banco de dados se não existir ainda."""
    try:
        db.session.add(obj)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        # Ignora a exception se for erro de chave primária duplicada
        if ("Duplicate entry" not in str(e)                 # Mysql
            and "UNIQUE constraint failed" not in str(e)):  # Sqlite
                raise e
    #    reason = e.message
    #    logger.warning(reason)

    #    if not ignore:
    #        raise e

    #    if "Duplicate entry" in reason:
    #        logger.info("%s already in table." % e.params[0])
    #        print(f"{e.params[0]} already in table.")
