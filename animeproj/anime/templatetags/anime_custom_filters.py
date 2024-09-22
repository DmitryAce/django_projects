from django import template


register = template.Library()


@register.filter
def pluralize_number(value, word):
    """Возвращает слово с правильным окончанием в зависимости от числа и масштаба."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return f"{value} голосов"

    if value < 1000:
        num = int(value)
    elif value < 1_000_000:
        num = int(value / 1_000)
    elif value < 1_000_000_000:
        num = int(value / 1_000_000)
    elif value < 1_000_000_000_000:
        num = int(value / 1_000_000_000)
    else:
        num = int(value / 1_000_000_000_000)

    if num == 1:
        return f"{num} {word}"
    elif num in [2, 3, 4]:
        return f"{num} {word}а"
    else:
        return f"{num} {word}ов"


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)