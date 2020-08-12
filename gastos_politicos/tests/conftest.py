import os
import json
import pytest

from gastos_politicos import create_app
from gastos_politicos.models import db


@pytest.fixture(scope="session")
def app():
    os.environ["APP_SETTINGS"] = "config.TestingConfig"
    app = create_app({"TESTING": True, "CACHE_NO_NULL_WARNING": True})
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


class Request:

    def __init__(self):
        self.path = ""
        self.headers = {}
        self.response = None

    def get(self, path="", headers={}):
        self.path = path
        self.headers = headers
        self.status_code = 200
        # Mapeia a url para o arquivo de fixture
        directory = os.path.join(os.path.dirname(__file__), "fixtures")
        if self.path.endswith("/api/v2/deputados"):
            self.response = os.path.join(directory, "deputados.json")
        elif "/api/v2/deputados/141459/despesas" in self.path:
            self.response = os.path.join(directory, "despesas.json")
        else:
            raise NotImplementedError
        return self

    def json(self):
        with open(self.response, "r") as f:
            return json.load(f)


@pytest.fixture
def requests():
    return Request()


@pytest.fixture
def politicos(client):
    from .fixtures.data import politicos
    db.session.bulk_save_objects(politicos)
    return politicos


@pytest.fixture
def reembolsos(client):
    from.fixtures.data import reembolsos
    db.session.bulk_save_objects(reembolsos)
    return reembolsos
