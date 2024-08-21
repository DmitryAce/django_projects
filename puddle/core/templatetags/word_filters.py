# myapp/templatetags/word_filters.py
from django import template

register = template.Library()

@register.filter
def pluralize(value, arg):
    """
    Возвращает слово с правильным окончанием в зависимости от значения.
    """
    if not isinstance(value, int):
        return value
    value = int(value)
    forms = arg.split(',')
    if len(forms) != 3:
        raise ValueError("Arg must contain three comma-separated forms")
    if value % 10 == 1 and value % 100 != 11:
        return f"{value} {forms[0]}"
    elif (value % 10 in [2, 3, 4] and not value % 100 in [12, 13, 14]):
        return f"{value} {forms[1]}"
    else:
        return f"{value} {forms[2]}"
