"""Integração simples com a api da câmara federal."""

import requests

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
HEADERS = {
    "accept": "application/json",
}


def deputados(fetch=requests.get):
    """Retorna os deputados da legislação atual."""
    r = fetch(f"{BASE_URL}/deputados", headers=HEADERS)
    assert r.status_code == 200
    return r.json()["dados"]


def despesas(deputado_id, mes=None, ano=None, fetch=requests.get):
    """Retorna as despesas do deputado."""
    url = (f"{BASE_URL}/deputados/{deputado_id}/despesas?"
           "ordem=DESC&ordenarPor=dataDocumento&itens=100")
    if ano is not None:
        url += f"&ano={ano}"
        # Aplica o filtro de mês somente se o ano for especificado
        if mes is not None:
            url += f"&mes={mes}"
    next = url
    while next is not None:
        print(next)
        resp = fetch(next, headers=HEADERS)
        assert resp.status_code == 200
        resp_json = resp.json()
        for despesa in resp_json.get("dados", []):
            yield despesa
        next = _next_page(resp_json)


def _next_page(json):
    for link in json.get("links"):
        if link.get("rel") == "next":
            return link.get("href")
