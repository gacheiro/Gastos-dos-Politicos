import pytest

from gastos_politicos.web.forms import form_filtro_despesas
from gastos_politicos.models import Politico


@pytest.mark.parametrize(("id", "result"), (
    (1, [("", "Todos os meses"), (8, "agosto"), (7, "julho")]),
    (2, [("", "Todos os meses"), (8, "agosto"), (5, "maio")]),
    (3, [("", "Todos os meses")]),
))
def test_form_filtro_despesas(app, politicos, reembolsos, id, result):
    """Testa se o formulário de filtrar reembolsos por mês é construído
       corretamente"""
    pol = Politico.query.get(id)
    with app.test_request_context():
        form = form_filtro_despesas(pol, 2020)
    assert form.mes.choices == result
