from datetime import datetime

import click
from flask_sqlalchemy import SQLAlchemy

from . import camara

db = SQLAlchemy()


def init_extensions(app):
    db.init_app(app)

    from app.models import Servidor, Despesa


    @app.cli.command("create-db")
    def create_db():
        """Cria as tabelas do banco de dados."""
        db.create_all()


    @app.cli.command("drop-db")
    def drop_db():
        """Deleta as tabelas do banco de dados."""
        db.drop_all()


    @app.cli.command("fetch-deps")
    def fetch_deps():
        dados = camara.deputados()
        for dep in dados:
            d = Servidor(
                id=dep["id"],
                nome=dep["nome"],
                email=dep["email"],
                partido=dep["siglaPartido"],
                uf=dep["siglaUf"],
                legislatura=dep["idLegislatura"],
            )
            db.session.merge(d)
        db.session.commit()


    @app.cli.command("fetch-desp")
    @click.option("--id", help="id do deputado.")
    def fetch_desp(id):
        if id:
            _despesas(id)
        else:
            for dep in [Servidor.query.first(),]:
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
                data_documento=datetime.strptime(desp["dataDocumento"], "%Y-%m-%d"),
                valor=desp["valorDocumento"],
                url_documento=desp["urlDocumento"],
                nome_fornecedor=desp["nomeFornecedor"],
                id_fornecedor=desp["cnpjCpfFornecedor"],
            )
            db.session.merge(d)
