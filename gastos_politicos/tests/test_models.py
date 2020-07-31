from gastos_politicos.models import Politico, Reembolso


def test_classificar_por(client):
    assert Politico.classificar_por(ano=2020) == []
    assert Politico.classificar_por(ano=2020, ordem="desc") == []


def test_total_gasto(client):
    assert Reembolso.total_gasto() == 0
