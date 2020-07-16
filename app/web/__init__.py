from . import pages, template_filters


def init_app(app):
    app.register_blueprint(pages.bp)
    # Registers template filters
    filters = (
        template_filters.month_abbr,
        template_filters.month_name,
        template_filters.currency,
    )
    for filter in filters:
        app.add_template_filter(filter)
