"""Integração simples com a api da câmara federal."""

import requests

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
HEADERS = {
    "accept": "application/json",
}


def deputados():
    """Retorna os deputados da legislação atual."""
    r = requests.get(f"{BASE_URL}/deputados", headers=HEADERS)
    return r.json()["dados"]


# TODO: obeter também a paginação completa, 
#       e não somente os primeiros 100 itens
def despesas(deputado_id, mes=None, ano=None):
    """Retorna as despesas do deputado."""
    url = (f"{BASE_URL}/deputados/{deputado_id}/despesas?"
           "ordem=DESC&ordenarPor=dataDocumento&itens=100")
    if mes is not None:
        url += f"&mes={mes}"
    if ano is not None:
        url += f"&ano={ano}"
    next = url
    while next is not None:
        print(next)
        resp = requests.get(next, headers=HEADERS)
        assert resp.status_code == 200
        resp_json = resp.json()
        for despesa in resp_json.get("dados", []):
            yield despesa
        next = _next_page(resp_json)


def _next_page(json):
    for link in json.get("links"):
        if link.get("rel") == "next":
            return link.get("href")
