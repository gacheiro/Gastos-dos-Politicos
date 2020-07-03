import locale
import calendar

locale.setlocale(locale.LC_ALL, "pt_BR")


def month_name(month):
    """Retorna o nome do mês. `month` pode ser int
    ou uma str representando um int"""
    try:
        month = int(month)
        return calendar.month_name[month]
    except (ValueError, IndexError):
        return ''


def month_abbr(month):
    """Retorna a abreviação do nome do mês. `month` pode ser int
    ou uma str representando um int"""
    try:
        month = int(month)
        return calendar.month_abbr[month]
    except (ValueError, IndexError):
        return ''


def currency(value, grouping=True, symbol=True):
    """Formata um valor para moeda."""
    try:
        return locale.currency(value, grouping=grouping, symbol=symbol)
    except (TypeError, ValueError):
        return ''


def init_app(app):
    for f in (month_name, month_abbr, currency):
        app.add_template_filter(f)
