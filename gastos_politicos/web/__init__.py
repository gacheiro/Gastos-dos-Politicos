from . import pages, template_utils


def init_app(app):
    app.register_blueprint(pages.bp)
    # Registra filtros de template
    filters = (
        template_utils.month_abbr,
        template_utils.month_name,
        template_utils.currency,
    )
    for filter in filters:
        app.add_template_filter(filter)
