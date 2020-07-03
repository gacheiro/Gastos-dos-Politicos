from . import pages
from . import template_filters

def init_app(app):
    app.register_blueprint(pages.bp)
    template_filters.init_app(app)
