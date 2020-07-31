from sqlalchemy import func, desc
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


class Politico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    partido = db.Column(db.String(10), nullable=True)
    uf = db.Column(db.String(2), nullable=False)
    legislatura = db.Column(db.Integer, nullable=False)
    url_foto = db.Column(db.String(250), nullable=True)

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
        ).all()

    @staticmethod
    def classificar_por(ano, mes=None, uf=None, partido=None,
                        ordem="desc", limite=-1):
        """Classifica os políticos pelo total gasto de acordo com os
        critérios de filtros. O parâmetro `ordem` pode ser 'asc' ou 'desc'.
        """
        query = db.session.query(
            Politico, func.sum(Reembolso.valor_liquido).label('total')
        ).join(Reembolso).filter_by(ano=ano).group_by(
            Politico.id
        )
        # Aplica os filtros opcionais
        if mes:
            query = query.filter(Reembolso.mes == mes)
        if uf:
            query = query.filter(Politico.uf == uf)
        if partido:
            query = query.filter(Politico.partido == partido)
        # Ordena por quem gastou mais ou gastou menos
        if ordem == "desc":
            query = query.order_by(desc('total'))
        else:
            query = query.order_by('total')
        return query.limit(limite).all()


class Reembolso(db.Model):
    # Para os reembolsos com serviços postais, o cod_documento costuma ser 0
    # O que dificulta usar somente o cod como chave primária
    # O num_documento algumas vezes é uma string longa (os nome do contradado, etc)
    cod_documento = db.Column(db.Integer, primary_key=True)
    num_documento = db.Column(db.String(100), primary_key=True)
    politico_id = db.Column(db.Integer, db.ForeignKey('politico.id'),
                            nullable=False)
    tipo = db.Column(db.String(250), nullable=False)
    tipo_documento = db.Column(db.String(30), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Numeric, nullable=False)
    valor_liquido = db.Column(db.Numeric, nullable=False)
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


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    feedback = db.Column(db.Text(500), nullable=False)
