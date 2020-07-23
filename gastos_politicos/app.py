import os
from flask import Flask
from . import ext, cli, web, models


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    ext.init_app(app)
    cli.init_app(app)
    web.init_app(app)
    models.init_app(app)
    return app
