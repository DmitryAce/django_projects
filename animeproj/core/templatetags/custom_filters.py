from django import template


register = template.Library()


@register.filter()
def replace_underscore(value):
    """Заменяет подчеркивания на пробелы в строке"""
    if isinstance(value, str):
        return value.replace("_", " ")
    return value


@register.filter
def humanize_number(value):
    """Адекватное представление чисел"""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < 1000:
        return str(value)
    elif value < 1_000_000:
        return f"{value / 1_000:.1f}k"
    elif value < 1_000_000_000:
        return f"{value / 1_000_000:.1f}M"
    elif value < 1_000_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    else:
        return f"{value / 1_000_000_000_000:.1f}T"


@register.filter
def truncate(value):
    """Сокращение длинных строк"""
    if (len(value) > 40):
        return value[:40]+"..."
    else: 
        return value


@register.filter
def listjoin(value, separator=' '):
    """Объединяет список строк в одну строку с указанным разделителем."""
    if isinstance(value, list):
        return separator.join(str(item) for item in value)
    elif hasattr(value, 'values_list'):
        return separator.join(str(item) for item in value.values_list('name', flat=True))
    return value


