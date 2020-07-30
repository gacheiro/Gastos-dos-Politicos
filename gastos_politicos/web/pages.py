from flask import (Blueprint, current_app, request,
                   redirect, url_for, render_template)

from gastos_politicos.ext.cache import cache
from gastos_politicos.models import db, Politico, Reembolso, Feedback
from .forms import form_filtro_despesas, FeedbackForm

bp = Blueprint("pages", __name__)


@bp.route("/")
@cache.cached() # Cache somente o index por enquanto
def index():
    """Retorna o index do site."""
    curr_month, curr_year = (current_app.config["CURRENT_MONTH"],
                             current_app.config["CURRENT_YEAR"])
    queries = {
        "total_gasto": Reembolso.total_gasto(ano=curr_year),
        "gastou_mais_mes": Politico.ranking(ano=curr_year, mes=curr_month),
        "gastou_mais": Politico.ranking(ano=curr_year),
        # Seleciona todos o politicos para usar no autocomplete
        "politicos": Politico.query.all(),
    }
    return render_template("pages/index.html", **queries)


@bp.route("/search", methods=["POST"])
def search():
    """Busca um politico pelo nome."""
    nome = request.form["nome"]
    p = Politico.query.filter_by(nome=nome).first()
    if p is None:
        return redirect(url_for("pages.index"))
    return redirect(url_for("pages.show", id=p.id))


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

    pagination = p.despesas(ano, mes).paginate(page, 40,
                                               error_out=True)
    total_gasto = Reembolso.total_gasto(p, ano=ano, mes=mes)
    return render_template("pages/show.html",
                           parlamentar=p,
                           pagination=pagination,
                           total_gasto=total_gasto,
                           form=form)


@bp.route("/sobre")
def about():
    form = FeedbackForm()
    return render_template("pages/about.html", form=form)


@bp.route("/feedback", methods=["POST"])
def feedback():
    """Cria um novo feedback."""
    form = FeedbackForm()
    if form.validate_on_submit():
        fb = Feedback(email=form.email.data,
                      feedback=form.feedback.data)
        db.session.add(fb)
        db.session.commit()
        # TODO: retornar uma flash message também
        return redirect(url_for("pages.about"))
    return render_template("pages/about.html", form=form)
