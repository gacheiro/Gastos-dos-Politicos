from sqlalchemy import func
from app.ext import db


class Servidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    partido = db.Column(db.String(10), nullable=True)
    uf = db.Column(db.String(2), nullable=False)
    legislatura = db.Column(db.Integer, nullable=False)
    url_foto = db.Column(db.String(250), nullable=True)

    def total_gasto(self, ano, mes=None):
        """Retorna o total gasto no `ano` e `mes` especificados.
        Se `mes` não for especificado, então considera todos os meses."""
        query = db.session.query(func.sum(Despesa.valor)) \
                          .filter_by(servidor=self, ano=ano)
        if mes is not None:
            query = query.filter_by(mes=mes)
        (total,) = query.first()      
        return total
    
    def despesas(self, ano=None, mes=None):
        """Retorna uma query com despesas do parlamentar
        filtradas por ano e mes."""
        query = Despesa.query.filter_by(servidor=self)
        if ano is not None:
            query = query.filter_by(ano=ano)
        if mes is not None:
            query = query.filter_by(mes=mes)
        return query.order_by(Despesa.data.desc())

    def gastos_por_mes(self, ano):
        """Retorna o valor gasto pelo parlamentar
        agrupado por mes no ano dado."""
        return db.session.query(Despesa.mes, func.sum(Despesa.valor)) \
                         .filter_by(servidor=self, ano=ano)           \
                         .group_by(Despesa.mes)                       \
                         .all()

    
class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servidor_id = db.Column(db.Integer, db.ForeignKey('servidor.id'),
                            nullable=False)
    tipo = db.Column(db.String(250), nullable=False)
    tipo_documento = db.Column(db.String(30), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Date, nullable=False)
    num_documento = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Numeric, nullable=False)
    url_documento = db.Column(db.String(250), nullable=True)
    nome_fornecedor = db.Column(db.String(250), nullable=False)
    id_fornecedor = db.Column(db.String(20), nullable=False)

    servidor = db.relationship('Servidor')
