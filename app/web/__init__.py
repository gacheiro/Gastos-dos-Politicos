from . import pages

def init_app(app):
    app.register_blueprint(pages.bp)
