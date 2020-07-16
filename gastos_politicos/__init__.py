import os
from flask import Flask


def create_app(config=None):
    from . import cli, web, models
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    cli.init_app(app)
    web.init_app(app)
    models.init_app(app)
    return app
