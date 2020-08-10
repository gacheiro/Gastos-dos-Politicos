import pytest

from gastos_politicos.web.template_utils import (month_name, month_abbr,
                                                 currency)


@pytest.mark.parametrize(("mes", "nome"), (
    (1,  "janeiro"), (2,  "fevereiro"), (3,  "março"),
    (4,  "abril"),   (5,  "maio"),      (6,  "junho"),
    (7,  "julho"),   (8,  "agosto"),    (9,  "setembro"),
    (10, "outubro"), (11, "novembro"),  (12, "dezembro"),
    ("", "")
))
def test_month_name(mes, nome):
    """Testa as formatações dos nomes dos meses."""
    assert month_name(mes) == nome


@pytest.mark.parametrize(("mes", "abrev"), (
    (1,  "jan"), (2,  "fev"), (3,  "mar"),
    (4,  "abr"), (5,  "mai"), (6,  "jun"),
    (7,  "jul"), (8,  "ago"), (9,  "set"),
    (10, "out"), (11, "nov"), (12, "dez"),
    ("", "")
))
def test_month_abbr(mes, abrev):
    """Testa as formatações das abreviações dos meses."""
    assert month_abbr(mes) == abrev


def test_currency():
    """Testa as formações em moeda."""
    # Aparentemente depende da versão do python o simbolo ser separado
    # ou não do valor (python locale)
    assert currency(114999.25) in ["R$ 114.999,00", "R$114.999,00"]
    # Quando verbose=True, não depende do locale
    assert currency(114999.25, verbose=True) == "R$ 114 MIL"
    assert currency(114, verbose=True) == "R$ 114"
    assert currency('NaN') == 'NaN'
    assert currency('NaN', verbose=True) == 'NaN'
