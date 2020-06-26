"""Integração com a api da câmara federal."""

import requests

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
HEADERS = {"accept": "application/json"}


def deputados():
    """Retorna os deputados da legislação atual."""
    r = requests.get(f"{BASE_URL}/deputados", headers=HEADERS)
    return r.json()["dados"]


def despesas(deputado_id):
    """Retorna as despesas do deputado."""
    url = f"{BASE_URL}/deputados/{deputado_id}/despesas?ordem=DESC&ordenarPor=dataDocumento&itens=100"
    r = requests.get(url, headers=HEADERS)
    return r.json()["dados"]
