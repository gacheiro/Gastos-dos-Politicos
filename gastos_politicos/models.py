from flask import current_app
from sqlalchemy import func, desc
from sqlalchemy.sql.expression import literal_column
from flask_sqlalchemy import SQLAlchemy

from gastos_politicos.ext.cache import cache

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


class Politico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    partido = db.Column(db.String(20), nullable=True)
    uf = db.Column(db.String(2), nullable=False)
    legislatura = db.Column(db.Integer, nullable=False)
    url_foto = db.Column(db.String(250), nullable=True)

    @staticmethod
    def lista_de_nomes():
        """Retorna a lista com os nomes de todos os políticos."""
        return [nome for (nome,) in db.session.query(Politico.nome).all()]

    def despesas(self, ano=None, mes=None):
        """Retorna uma query com despesas do parlamentar
        filtradas por ano e mes."""
        query = Reembolso.query.filter_by(politico=self)
        if ano is not None:
            query = query.filter_by(ano=ano)
        if mes is not None:
            query = query.filter_by(mes=mes)
        return query.order_by(Reembolso.data.desc())

    def gastos_por_mes(self, ano):
        """Retorna uma lista de tuplas (mês, total_gasto) com os gastos
        mensais do parlamentar."""
        return db.session.query(
            Reembolso.mes, func.sum(Reembolso.valor_liquido)
        ).filter_by(politico=self, ano=ano).group_by(
            Reembolso.mes
        ).order_by(Reembolso.mes.desc()).all()

    @staticmethod
    @cache.memoize()
    def classificar_por(ano, mes=None, uf=None, partido=None,
                        ordem="desc", limite=513):
        """Classifica os políticos pelo total gasto de acordo com os
        critérios de filtros. O parâmetro `ordem` pode ser 'asc' ou 'desc'.
        """
        subquery = db.session.query(
            Reembolso.politico_id,
            func.sum(Reembolso.valor_liquido).label("total")
        ).filter_by(ano=ano).group_by(
            Reembolso.politico_id
        )
        # Aplica os filtros opcionais na subquery
        if mes:
            subquery = subquery.filter(Reembolso.mes == mes)
        # Query principal
        query = db.session.query(
            Politico, literal_column("total")).join(subquery.subquery())
        # Aplica os filtros opcionais na query principal
        if uf:
            query = query.filter(Politico.uf == uf)
        if partido:
            query = query.filter(Politico.partido == partido)
        # Ordena por quem gastou mais ou gastou menos
        if ordem == "desc":
            query = query.order_by(desc(literal_column("total")))
        else:
            query = query.order_by(literal_column("total"))
        query = query.limit(limite)
        current_app.logger.info(query)
        return query.all()


class Reembolso(db.Model):
    # Para os reembolsos com serviços postais, o cod_documento costuma ser 0
    # O que dificulta usar somente o cod como chave primária
    # O num_documento algumas vezes é uma string longa (os nome do contradado, etc)
    cod_documento = db.Column(db.Integer, primary_key=True)
    num_documento = db.Column(db.String(100), primary_key=True)
    politico_id = db.Column(db.Integer, db.ForeignKey('politico.id'),
                            nullable=False, index=True)
    tipo = db.Column(db.String(250), nullable=False)
    tipo_documento = db.Column(db.String(30), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    valor_liquido = db.Column(db.Float, nullable=False)
    url_documento = db.Column(db.String(250), nullable=True)
    nome_fornecedor = db.Column(db.String(250), nullable=False)
    id_fornecedor = db.Column(db.String(20), nullable=False)

    politico = db.relationship('Politico')

    @staticmethod
    def total_gasto(politico=None, ano=None, mes=None):
        """Retorna a soma de todos os gasto de acordo
        com os filtros especificados."""
        query = db.session.query(func.sum(Reembolso.valor_liquido))
        if politico is not None:
            query = query.filter_by(politico=politico)
        if ano is not None:
            query = query.filter_by(ano=ano)
        if mes is not None:
            query = query.filter_by(mes=mes)
        # Retorna 0 caso o valor total seja None (banco de dados vazio)
        return query.scalar() or 0

    @staticmethod
    @cache.memoize()
    def mais_recentes(acima_de=0, n=10):
        """Retorna os `n` reembolsos mais recentes acima do valor especifico."""
        return Reembolso.query.filter(
            Reembolso.valor_liquido > acima_de
        ).order_by(Reembolso.data.desc()).limit(n).all()


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    feedback = db.Column(db.Text(500), nullable=False)
