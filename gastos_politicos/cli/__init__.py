from .commands import (create_db, drop_db, clear_cache,
                       obter_deputados, obter_despesas)

commands = [
    create_db,
    drop_db,
    clear_cache,
    obter_deputados,
    obter_despesas,
]

def init_app(app):
    for command in commands:
        app.cli.add_command(app.cli.command()(command))
