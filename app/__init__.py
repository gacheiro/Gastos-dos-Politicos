import os
from flask import Flask

from app.ext import init_extensions
import app.cli as cli
import app.web as web


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    init_extensions(app)
    cli.init_app(app)
    web.init_app(app)
    return app
