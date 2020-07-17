from gastos_politicos.models import Politico, Reembolso


def test_ranking(client):
    assert Politico.ranking(ano=2020) == []
    assert Politico.ranking(ano=2020, reverso=True) == []


def test_total_gasto(client):
    assert Reembolso.total_gasto() == 0
