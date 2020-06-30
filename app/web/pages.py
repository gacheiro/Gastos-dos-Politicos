from flask import Blueprint, request, render_template

from app.models import Servidor, Despesa

bp = Blueprint("pages", __name__)


@bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    query = Despesa.query.order_by(Despesa.data.desc())
    pagination = query.paginate(page, 50, error_out=True)
    return render_template("pages/index.html", pagination=pagination)


@bp.route("/p/<int:id>")
def show(id):
    """Retorna as despesas de um político específico."""
    mes, ano, page = (request.args.get("mes"),
                      request.args.get("ano", 2020),
                      request.args.get("page", 1, type=int))
    p = Servidor.query.get_or_404(id)
    pagination = (p.despesas(ano, mes)
                  .order_by(Despesa.data.desc())
                  .paginate(page, 50, error_out=True))
    return render_template("pages/show.html", 
                           parlamentar=p,
                           navigation=p.gastos_por_mes(ano),
                           pagination=pagination)
