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
    app.shell_context_processor(shell_context)
    return app


def shell_context():
    """Exporta algumas classes para usar no flask shell."""
    from .models import db, Politico, Reembolso, Feedback
    return dict(db=db, Politico=Politico,
                Reembolso=Reembolso, Feedback=Feedback)
