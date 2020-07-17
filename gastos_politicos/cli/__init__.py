from datetime import datetime

import click

from ..models import db, Politico, Reembolso
from . import camara


def create_db():
    """Cria as tabelas do banco de dados."""
    db.create_all()


def drop_db():
    """Deleta as tabelas do banco de dados."""
    db.drop_all()


def obter_deputados():
    """Popula o banco de dados com os deputados da legislação atual."""
    dados = camara.deputados()
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
        db.session.merge(d)
    db.session.commit()


@click.option("--id", help="id do politico.")
@click.option("--mes", help="mês das despesas.")
@click.option("--ano", help="ano das despesas.")
def obter_despesas(id, ano, mes):
    """Popula o banco de dados com as últimas despesas dos deputados."""
    print(f"obter-despesas --id {id} --ano {ano} --mes {mes}")        
    if id:
        _fetch_desp(id, mes, ano)
    else:
        query = Politico.query.order_by(Politico.nome)
        for i, p in enumerate(query.all(), 1):
            print(f"{i} - [{p.id}] Obtendo as despesas de {p.nome}.")
            _fetch_desp(p.id, mes, ano)
    db.session.commit()
    print("Atualização completa.")


def _fetch_desp(id, mes, ano):
    dados = camara.despesas(id, mes=mes, ano=ano)
    for desp in dados:
        # Algumas despesas têm dataDocumento=null, apenas ignore por enquanto
        # TODO: reconstruir a data da despesa com o ano e o mês
        if desp["dataDocumento"] is None:
            print(f"Ignorando despesa sem data {desp['codDocumento']}")
            continue
        d = Reembolso(
            politico_id=id,
            id=desp["codDocumento"],
            tipo=desp["tipoDespesa"],
            tipo_documento=desp["tipoDocumento"],
            num_documento=desp["numDocumento"],
            ano=desp["ano"],
            mes=desp["mes"],
            data=datetime.strptime(desp["dataDocumento"], "%Y-%m-%d"),
            valor=desp["valorDocumento"],
            url_documento=desp["urlDocumento"],
            nome_fornecedor=desp["nomeFornecedor"],
            id_fornecedor=desp["cnpjCpfFornecedor"],
        )
        db.session.merge(d)


def init_app(app):
    for command in (create_db, drop_db, obter_deputados, obter_despesas):
        app.cli.add_command(app.cli.command()(command))
