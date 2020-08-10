import pytest

from gastos_politicos.models import Politico, Reembolso


def test_classificar_por(client):
    assert Politico.classificar_por(ano=2020) == []
    assert Politico.classificar_por(ano=2020, ordem="desc") == []


def test_total_gasto(client):
    assert Reembolso.total_gasto() == 0


@pytest.mark.parametrize(("n", "acima_de", "result"), (
    (5, 0, []),
    (5, 1000, []),
))
def test_mais_recentes(client, n, acima_de, result):
    assert Reembolso.mais_recentes(n, acima_de) == result
