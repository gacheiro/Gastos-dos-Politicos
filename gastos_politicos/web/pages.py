from flask import Blueprint, request, redirect, url_for, render_template

from gastos_politicos.ext.cache import cache
from ..models import Politico, Reembolso
from .forms import form_filtro_despesas

bp = Blueprint("pages", __name__)


@bp.route("/")
@cache.cached() # Cache somente o index por enquanto
def index():
    total_gasto = Reembolso.total_gasto()
    quem_gastou_mais = Politico.ranking()
    quem_gastou_menos = Politico.ranking(reverso=True)
    return render_template("pages/index.html",
                           total_gasto=total_gasto,
                           quem_gastou_mais=quem_gastou_mais,
                           quem_gastou_menos=quem_gastou_menos)


@bp.route("/p/<int:id>", methods=["GET", "POST"])
def show(id):
    """Retorna as despesas de um parlamentar específico."""
    p = Politico.query.get_or_404(id)
    # Aplica os filtros de mes, ano e a paginação
    mes, ano, tipo, page = (request.args.get("mes"),
                            request.args.get("ano", 2020, type=int),
                            request.args.get("tipo"),
                            request.args.get("page", 1, type=int))

    form = form_filtro_despesas(parlamentar=p, ano=ano)
    if form.validate_on_submit():
        # Retira os filtros do tipo `mes=""` (Todos os meses)
        # Deixa somente os definidos como `mes=1`, etc.
        # Depois redireciona para aplicar os filtros
        params = {k: v for k, v in form.data.items() if v}
        # Remove o csrf_token antes de redirecionar
        params.pop("csrf_token")
        return redirect(url_for("pages.show", id=id, **params))

    pagination = p.despesas(ano, mes).paginate(page, 50,
                                               error_out=True)
    total_gasto = Reembolso.total_gasto(p, ano=ano, mes=mes)
    return render_template("pages/show.html",
                           parlamentar=p,
                           pagination=pagination,
                           total_gasto=total_gasto,
                           form=form)


@bp.route("/sobre")
def about():
    return render_template("pages/about.html")
