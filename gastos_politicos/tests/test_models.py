import pytest

from gastos_politicos.models import Politico, Reembolso


def test_lista_de_nomes(politicos):
    """Testa o método que retorna a lista de nomes de todos os políticos."""
    assert Politico.lista_de_nomes() == [
        "Politico 01",
        "Politico 02",
        "Politico 03",
        "Politico 04",
        "Politico 05",
    ]


@pytest.mark.parametrize(("id", "ano", "mes", "count"), (
    (1, 2020, None, 3),
    (1, 2020, 7,    1),
    (1, 2020, 8,    2),
    (1, None, 7,    1),
    (1, None, 8,    2),
))
def test_despesas(politicos, reembolsos, id, ano, mes, count):
    """Testa o método para obter despesas de um político."""
    pol = Politico.query.get(id)
    assert pol.despesas(ano=ano, mes=mes).count() == count


@pytest.mark.parametrize(("id", "result"), (
    (1, [(8, 6540.2), (7, 215.3)]),
    (2, [(8, 280), (5, 2000)]),
    (3, []),
))
def test_gastos_por_mes(politicos, reembolsos, id, result):
    """Testa o método que retorna os gastos agrupados por mês."""
    pol = Politico.query.get(id)
    assert pol.gastos_por_mes(2020) == result


@pytest.mark.parametrize(("mes", "uf", "partido", "ordem", "result"), (
    (None, None, None,         "desc", [(1, 6755.5), (2, 2280)]),
    (None, None, None,         "asc",  [(2, 2280), (1, 6755.5)]),
    (8,    "SP", None,         "desc", [(1, 6540.2)]),
    (8,    None, "Partido 01", "desc", [(1, 6540.2), (2, 280)]),
))
def test_classificar_por(politicos, reembolsos, mes, uf, partido, ordem, result):
    r = Politico.classificar_por(ano=2020, mes=mes, uf=uf, partido=partido,
                                 ordem=ordem)
    ids = [(p.id, v) for p, v in r]
    assert ids == result


@pytest.mark.parametrize(("id", "ano", "mes", "total"), (
    (-1, None, None, 9035.5),
    (1,  None, None, 6755.5),
    (1,  2020, None, 6755.5),
    (1,  2020, 8,    6540.2),
    (2,  2020, None, 2280),
))
def test_total_gasto(politicos, reembolsos, id, ano, mes, total):
    pol = Politico.query.get(id)
    assert Reembolso.total_gasto(politico=pol, ano=ano, mes=mes) == total


@pytest.mark.parametrize(("n", "acima_de", "result"), (
    (3, 0,    [7003506, 7003408, 7014746]),
    (3, 1000, [7014746, 7010948]),
))
def test_mais_recentes(politicos, reembolsos, n, acima_de, result):
    cods = [r.cod_documento for r in Reembolso.mais_recentes(n=n,
                                                             acima_de=acima_de)]
    assert cods == result
