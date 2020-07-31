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

# Por algum motivo o WTForms não aceita o SelectField com choices apenas com
# valores. Por esse motivo as choices estão com chave, valor iguais
ufs_choices = [
    ('', 'Todas'), ('AC', 'AC'), ('AL', 'AL'), ('AM', 'AM'), ('AP', 'AP'),
    ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'),
    ('MA', 'MA'), ('MG', 'MG'), ('MS', 'MS'), ('MT', 'MT'), ('PA', 'PA'),
    ('PB', 'PB'), ('PE', 'PE'), ('PI', 'PI'), ('PR', 'PR'), ('RJ', 'RJ'),
    ('RN', 'RN'), ('RO', 'RO'), ('RR', 'RR'), ('RS', 'RS'), ('SC', 'SC'),
    ('SE', 'SE'), ('SP', 'SP'), ('TO', 'TO'),
]

partidos_choices = [
    ('', 'Todos'), ('AVANTE', 'AVANTE'), ('CIDADANIA', 'CIDADANIA'),
    ('DEM', 'DEM'), ('MDB', 'MDB'), ('NOVO', 'NOVO'), ('PATRIOTA', 'PATRIOTA'),
    ('PCdoB', 'PCdoB'), ('PDT', 'PDT'), ('PL', 'PL'), ('PODE', 'PODE'),
    ('PP', 'PP'), ('PROS', 'PROS'), ('PSB', 'PSB'), ('PSC', 'PSC'),
    ('PSD', 'PSD'), ('PSDB', 'PSDB'), ('PSL', 'PSL'), ('PSOL', 'PSOL'),
    ('PT', 'PT'), ('PTB', 'PTB'), ('PV', 'PV'), ('REDE', 'REDE'),
    ('REPUBLICANOS', 'REPUBLICANOS'), ('SOLIDARIEDADE', 'SOLIDARIEDADE')
]


class BuscaPoliticoForm(FlaskForm):
    """Formulário para buscar um político específico."""

    class Meta:
        """Desativa o csrf_token."""
        csrf = False

    nome = SearchField("Nome", validators=[
        Length(max=100),
    ])
    uf = SelectField("UF", choices=ufs_choices)
    partido = SelectField("Partido", choices=partidos_choices)

    def validate_on_submit(self):
        """Garante que pelo menos um campo tenha sido fornecido na busca."""
        return (super().validate_on_submit()
                and (self.nome.data or self.uf.data or self.partido.data))


class FeedbackForm(FlaskForm):
    """Formulário para envio de feedback."""
    email = EmailField("Email", validators=[
        InputRequired(), Length(max=100),
    ])
    feedback = TextAreaField("Fale conosco", validators=[
        InputRequired(), Length(max=500),
    ])
