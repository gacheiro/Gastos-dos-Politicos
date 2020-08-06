from gastos_politicos.cli.dados_abertos import deputados, despesas, _next_page


def test_deputados(requests):
    """Testa a função que busca os dados dos deputados."""
    deps = deputados(fetch=requests.get)
    assert requests.path == "https://dadosabertos.camara.leg.br/api/v2/deputados"
    assert requests.headers.get("accept") == "application/json"
    assert deps == requests.json()["dados"]


def test_despesas(requests):
    """Testa a função que busca as despesas de um deputado."""
    base_url = (
        "https://dadosabertos.camara.leg.br/api/v2/deputados/"
        "141459/despesas?ordem=DESC&ordenarPor=dataDocumento&itens=100"
    )
    desps = list(despesas(141459, ano=2020, mes=1, fetch=requests.get))
    assert requests.path == f"{base_url}&ano=2020&mes=1"
    assert requests.headers.get("accept") == "application/json"
    assert desps == requests.json()["dados"]

    # Pesquisa sem o mês
    desps = list(despesas(141459, ano=2020, fetch=requests.get))
    assert requests.path == f"{base_url}&ano=2020"
    assert desps == requests.json()["dados"]

    # Pesquisa sem o ano (ignora o mês)
    desps = list(despesas(141459, mes=1, fetch=requests.get))
    assert requests.path == base_url
    assert desps == requests.json()["dados"]


def test_next_page():
    """Testa a navegação na paginação da api."""
    r = {
        "links": [
            {
                "rel": "next",
                "href": "https://dadosabertos.camara.leg.br/api/v2/..."
            }
        ]
    }
    assert _next_page(r) == "https://dadosabertos.camara.leg.br/api/v2/..."

    s = {
        "links": [
            {
                "rel": "self",
                "href": "https://dadosabertos.camara.leg.br/api/v2/..."
            }
        ]
    }
    assert _next_page(s) == None
