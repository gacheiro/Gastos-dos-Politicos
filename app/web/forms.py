from flask_wtf import FlaskForm
from wtforms import SelectField


class FiltroDespesas(FlaskForm):
    ano = SelectField("Ano", choices=[
        ("2020", 2020)
    ])
    mes = SelectField("Mês", choices=[
        ("", "Todos os meses"),
        ("1", 1)
    ])
    tipo = SelectField("Tipo", choices=[
        ("", "Todos os tipos")
    ])
