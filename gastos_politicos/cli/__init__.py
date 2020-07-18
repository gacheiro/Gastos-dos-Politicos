from .commands import create_db, drop_db, obter_deputados, obter_despesas


def init_app(app):
    for command in (create_db, drop_db, obter_deputados, obter_despesas):
        app.cli.add_command(app.cli.command()(command))
