from flask import Blueprint, request, redirect, url_for, render_template

from app.models import Servidor, Despesa
from .forms import FiltroDespesas

bp = Blueprint("pages", __name__)


@bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    query = Despesa.query.order_by(Despesa.data.desc())
    pagination = query.paginate(page, 50, error_out=True)
    return render_template("pages/index.html", pagination=pagination)


@bp.route("/p/<int:id>", methods=["POST", "GET"])
def show(id):
    """Retorna as despesas de um parlamentar específico."""
    p = Servidor.query.get_or_404(id)
    form = FiltroDespesas()
    if form.validate_on_submit():
        # Retira os filtros do tipo `mes=""` (Todos os meses)
        # Deixa somente os definidos como `mes=1`, etc.
        # Depois redireciona para aplicar os filtros
        params = {k: v for k, v in form.data.items() if v}
        # Remove o csrf_token antes de redirecionar
        params.pop("csrf_token")
        return redirect(url_for("pages.show", id=id, **params))

    # Aplica os filtros de mes, ano e a paginação
    mes, ano, tipo, page = (request.args.get("mes"),
                            request.args.get("ano", 2020),
                            request.args.get("tipo"),
                            request.args.get("page", 1, type=int))
    pagination = (p.despesas(ano, mes)
                  .order_by(Despesa.data.desc())
                  .paginate(page, 50, error_out=True))
    return render_template("pages/show.html", 
                           parlamentar=p,
                           pagination=pagination,
                           form=form)
