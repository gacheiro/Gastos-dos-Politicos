"""Integração simples com a api da câmara federal."""

import requests

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
HEADERS = {"accept": "application/json"}


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
    r = requests.get(url, headers=HEADERS)
    return r.json()["dados"]
