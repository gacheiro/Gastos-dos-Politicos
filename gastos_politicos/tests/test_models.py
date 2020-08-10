import pytest

from gastos_politicos.models import Politico, Reembolso


@pytest.mark.parametrize(("ano", "ordem", "result"), (
    (2020, None, []),
    (2020, "desc", []),
))
def test_classificar_por(client, ano, ordem, result):
    assert Politico.classificar_por(ano=ano, ordem=ordem) == result


def test_total_gasto(client):
    assert Reembolso.total_gasto() == 0


@pytest.mark.parametrize(("n", "acima_de", "result"), (
    (5, 0, []),
    (5, 1000, []),
))
def test_mais_recentes(client, n, acima_de, result):
    assert Reembolso.mais_recentes(n, acima_de) == result
