from app.ext import db


class Servidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    partido = db.Column(db.String(10), nullable=True)
    uf = db.Column(db.String(2), nullable=False)
    legislatura = db.Column(db.Integer, nullable=False)
    url_foto = db.Column(db.String(250), nullable=True)


class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servidor_id = db.Column(db.Integer, db.ForeignKey('servidor.id'),
                            nullable=False)
    tipo = db.Column(db.String(250), nullable=False)
    tipo_documento = db.Column(db.String(30), nullable=False)
    data = db.Column(db.Date, nullable=False)
    num_documento = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Numeric, nullable=False)
    url_documento = db.Column(db.String(250), nullable=True)
    nome_fornecedor = db.Column(db.String(250), nullable=False)
    id_fornecedor = db.Column(db.String(20), nullable=False)

    servidor = db.relationship('Servidor')
