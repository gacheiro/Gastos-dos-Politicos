from flask import g

from gastos_politicos.models import Feedback


def test_index(client):
    """Testa o index."""
    rv = client.get("/")
    assert rv.status_code == 200


def test_about(client):
    """Testa a página Sobre."""
    rv = client.get("/")
    assert rv.status_code == 200


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
