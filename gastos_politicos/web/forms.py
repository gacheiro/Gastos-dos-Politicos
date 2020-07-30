from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.fields.html5 import EmailField, SearchField
from wtforms.validators import InputRequired, Length

from .template_utils import month_name


def form_filtro_despesas(parlamentar, ano):
    """Cria e define os meses dinamicamente de acordo com as despesas."""
    form = FiltroDespesasForm()
    for mes, _ in parlamentar.gastos_por_mes(ano):
        choice = mes, month_name(mes)
        form.mes.choices.append(choice)
    return form


class FiltroDespesasForm(FlaskForm):
    """Formulário para o filtro de despesas na página do politico.
    Os dados dos selects são carregados dinamicamente na view.
    """
    ano = SelectField("Ano", choices=[
        ("2020", 2020),
    ])
    mes = SelectField("Mês", choices=[
        ("", "Todos os meses"),
    ], validate_choice=False)
    tipo = SelectField("Tipo", choices=[
        ("", "Todos os tipos"),
    ])


class BuscaPoliticoForm(FlaskForm):
    """Formulário para buscar um político específico."""

    class Meta:
        """Desativa o csrf_token."""
        csrf = False

    nome = SearchField("Nome", validators=[
        InputRequired(), Length(max=100),
    ])


class FeedbackForm(FlaskForm):
    """Formulário para envio de feedback."""
    email = EmailField("Email", validators=[
        InputRequired(), Length(max=100),
    ])
    feedback = TextAreaField("Fale conosco", validators=[
        InputRequired(), Length(max=500),
    ])
