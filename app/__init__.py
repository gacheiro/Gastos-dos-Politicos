import os
from flask import Flask

import app.web as web
from app.ext import init_extensions


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    init_extensions(app)
    web.init_app(app)
    return app
