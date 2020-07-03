from flask_wtf import FlaskForm
from wtforms import SelectField

from .template_filters import month_name


def form_filtro_despesas(parlamentar, ano):
    """Cria e define os meses dinamicamente de acordo com as despesas."""
    form = FiltroDespesas()
    print(ano)
    for mes, _ in parlamentar.gastos_por_mes(ano):
        choice = mes, month_name(mes)
        form.mes.choices.append(choice)
    return form


class FiltroDespesas(FlaskForm):
    ano = SelectField("Ano", choices=[
        ("2020", 2020),
    ])
    mes = SelectField("Mês", choices=[
        ("", "Todos os meses"),
    ], validate_choice=False)
    tipo = SelectField("Tipo", choices=[
        ("", "Todos os tipos"),
    ])
