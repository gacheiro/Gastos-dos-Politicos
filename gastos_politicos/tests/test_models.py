from gastos_politicos.models import Servidor, Despesa


def test_total_gasto(client):
    assert Despesa.total_gasto() == 0
