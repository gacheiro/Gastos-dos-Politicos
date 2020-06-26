from flask import Blueprint, render_template

from app.models import Servidor, Despesa

bp = Blueprint('pages', __name__)


@bp.route('/')
def index():
    despesas = Despesa.query.order_by(Despesa.data_documento.desc()).all()
    return render_template('pages/index.html', despesas=despesas)


def init_app(app):
    app.register_blueprint(bp)
