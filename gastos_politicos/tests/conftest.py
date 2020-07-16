import os
import pytest

from gastos_politicos import create_app
from gastos_politicos.models import db


@pytest.fixture
def client():
    os.environ['APP_SETTINGS'] = 'config.TestingConfig'
    app = create_app()
    assert app.config['TESTING']
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()
