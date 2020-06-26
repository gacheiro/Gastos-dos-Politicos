from flask import Blueprint, request, render_template

from app.models import Servidor, Despesa

bp = Blueprint("pages", __name__)


@bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    query = Despesa.query.order_by(Despesa.data.desc())
    pagination = query.paginate(page, 50, error_out=True)
    return render_template("pages/index.html", pagination=pagination)
