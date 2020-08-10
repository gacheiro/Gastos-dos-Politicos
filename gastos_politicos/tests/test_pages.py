import pytest
from flask import g

from gastos_politicos.models import Feedback


def test_index(client):
    """Testa o index."""
    rv = client.get("/")
    assert rv.status_code == 200


@pytest.mark.parametrize(("nome", "uf", "partido", "codigo"), (
    ("", "", "", 302),      # Redirecionado para o index
    ("NOME", "", "", 302),  # Redirecionado para página do político
))
def test_search_redirect(client, nome, uf, partido, codigo):
    rv = client.post("/q", data=dict(nome=nome, uf=uf, partido=partido))
    assert rv.status_code == codigo


@pytest.mark.parametrize(("nome", "uf", "partido", "texto"), (
    ("NOME", "SP", "",     b"TODOS OS PARTIDOS / SP"),
    ("NOME", "",   "REDE", b"REDE / TODOS OS ESTADOS"),
    ("NOME", "SP", "REDE", b"REDE / SP"),
))
def test_search_filter(client, nome, uf, partido, texto):
    """Testa a busca por políticos."""
    rv = client.post("/q", data=dict(nome=nome, uf=uf, partido=partido))
    assert rv.status_code == 200
    # Testa alguns elementos no html retornado
    assert texto in rv.data


def test_about(client):
    """Testa a página Sobre."""
    rv = client.get("/sobre")
    assert rv.status_code == 200
    assert "<title>Gastos dos Políticos - Sobre</title>".encode() in rv.data


def test_feedback(client):
    """Testa o envio de feedback pela página Sobre."""
    assert Feedback.query.count() == 0
    rv = client.get("/sobre")
    signed_token = g.csrf_token
    rv = client.post("/feedback", data=dict(
                        email="email@example.com",
                        feedback="This is a feedback.",
                        csrf_token=signed_token,
                    ), follow_redirects=True)
    assert rv.status_code == 200
    assert Feedback.query.count() == 1
    fb = Feedback.query.one()
    assert fb.email == "email@example.com"
    assert fb.feedback == "This is a feedback."


def test_invalid_feedback(client):
    rv = client.get("/sobre")
    signed_token = g.csrf_token
    rv = client.post("/feedback", data=dict(
                        email="",
                        feedback="This is a feedback.",
                        csrf_token=signed_token))
    assert Feedback.query.count() == 0
