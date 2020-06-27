from datetime import datetime

import click

from app.models import db, Servidor, Despesa
from . import camara


def create_db():
    """Cria as tabelas do banco de dados."""
    db.create_all()


def drop_db():
    """Deleta as tabelas do banco de dados."""
    db.drop_all()


def fetch_deps():
    """Popula o banco de dados com os deputados da legislação atual."""
    dados = camara.deputados()
    for dep in dados:
        d = Servidor(
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


@click.option("--id", help="id do deputado.")
def fetch_desp(id):
    """Popula o banco de dados com as últimas despesas dos deputados."""
    if id:
        _despesas(id)
    else:
        for dep in [Servidor.query.get(204453), Servidor.query.get(74646)]:
            print(f"Obtendo as despesas de {dep.nome}...")
            _despesas(dep.id)
    db.session.commit()


def _despesas(id):
    dados = camara.despesas(id)
    for desp in dados:
        d = Despesa(
            servidor_id=id,
            id=desp["codDocumento"],
            tipo=desp["tipoDespesa"],
            tipo_documento=desp["tipoDocumento"],
            num_documento=desp["numDocumento"],
            data=datetime.strptime(desp["dataDocumento"], "%Y-%m-%d"),
            valor=desp["valorDocumento"],
            url_documento=desp["urlDocumento"],
            nome_fornecedor=desp["nomeFornecedor"],
            id_fornecedor=desp["cnpjCpfFornecedor"],
        )
        db.session.merge(d)


def init_app(app):
    for command in (create_db, drop_db, fetch_deps, fetch_desp):
        app.cli.add_command(app.cli.command()(command))
