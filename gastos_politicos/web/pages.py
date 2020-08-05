from flask import (Blueprint, current_app, request,
                   redirect, url_for, render_template)

from gastos_politicos.ext.cache import cache
from gastos_politicos.models import db, Politico, Reembolso, Feedback
from .forms import form_filtro_despesas, BuscaPoliticoForm, FeedbackForm

bp = Blueprint("pages", __name__)


@bp.route("/")
def index():
    """Renderiza o index do site."""
    mes, ano, limite = (current_app.config["CURRENT_MONTH"],
                        current_app.config["CURRENT_YEAR"], 7)
    kwargs = {
        "total_gasto": Reembolso.total_gasto(ano=ano),
        "gastou_mais_mes": Politico.classificar_por(ano=ano, mes=mes,
                                                    limite=limite),
        "gastou_mais": Politico.classificar_por(ano=ano, limite=limite),
        # Seleciona os nomes dos politicos para usar no autocomplete
        "datalist": Politico.lista_de_nomes(),
        # Formulário para buscar um político específico
        "form": BuscaPoliticoForm(),
    }
    return render_template("pages/index.html", **kwargs)


@bp.route("/q", methods=["GET", "POST"])
def search():
    """Busca um politico pelo nome ou filtra por uf e partido. Se uf ou partido
    forem especificados, então ignora o campo nome e renderiza a lista de
    políticos que correspondem à uf e/ou partido. Se somente nome for
    especificado, tentará redirecionar para o página do político.
    """
    form = BuscaPoliticoForm()
    nome, uf, partido = form.nome.data, form.uf.data, form.partido.data
    current_app.logger.info(
        f"Busca por nome='{nome}' uf='{uf}' e partido='{partido}'.")

    if not form.validate_on_submit():
        return redirect(url_for("pages.index"))
    # Filtra por uf e partido
    elif uf or partido:
        query = Politico.classificar_por(ano=current_app.config["CURRENT_YEAR"],
                                         uf=uf, partido=partido)
        return render_template(
            "pages/filter.html",
            ranking=query,
            # Nomes necessários para o autocomplete
            datalist=Politico.lista_de_nomes(),
            form=form,
        )
    # Tenta redirecionar para um político específico
    # Retorna para o index se nenhum for encontrado
    p = Politico.query.filter(Politico.nome.ilike(f"%{nome}%")).first()
    return (redirect(url_for("pages.show", id=p.id)) if p
            else redirect(url_for("pages.index")))


@bp.route("/p/<int:id>", methods=["GET", "POST"])
def show(id):
    """Renderiza a página de um político específico."""
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
    """Renderiza a página Sobre."""
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
