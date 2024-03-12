import os
import locale
import calendar

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


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


def currency(value, grouping=True, symbol=True, verbose=False):
    """Formata um valor para moeda.
       Use verbose=True para formatar o valor para um formato verboso:
       114_999|currency => R$ 114.000,00
       114_999|currency(verbose=True) => R$ 114 MIL
    """
    try:
        value = int(value)
        if verbose:
            suffix = ""
            if value >= 1000:
                value //= 1000
                suffix = " MIL"
            return f"R$ {value}{suffix}"
        else:
            return locale.currency(value, grouping=grouping, symbol=symbol)
    except (TypeError, ValueError):
        return 'NaN'
