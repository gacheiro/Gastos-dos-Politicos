from flask import g

from gastos_politicos.models import Feedback


def test_index(client):
    """Testa o index."""
    rv = client.get("/")
    assert rv.status_code == 200


def test_search_redirect(client):
    rv = client.post("/q", data=dict(nome="", uf="", partido=""))
    assert rv.status_code == 302    # Redirecionado para o index
    rv = client.post("/q", data=dict(nome="NOME", uf="", partido=""))
    assert rv.status_code == 302    # Redireciona para página do político


def test_search_filter(client):
    """Testa a busca por políticos."""
    # Rederiza o filter.html
    # Testa alguns elementos no html retornado
    rv = client.post("/q", data=dict(nome="NOME", uf="SP", partido=""))
    assert rv.status_code == 200
    print(rv.data)
    assert b"TODOS OS PARTIDOS / SP" in rv.data
    rv = client.post("/q", data=dict(nome="NOME", uf="", partido="REDE"))
    assert rv.status_code == 200
    assert b"REDE / TODOS OS ESTADOS" in rv.data
    rv = client.post("/q", data=dict(nome="NOME", uf="SP", partido="REDE"))
    assert rv.status_code == 200
    assert b"REDE / SP" in rv.data


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
