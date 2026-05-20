from datetime import datetime, timezone, timedelta

# Zona horaria de Colombia (UTC-5)
COLOMBIA_TZ = timezone(timedelta(hours=-5))


def colombia_now():
    """Retorna la hora actual en Colombia (UTC-5) como datetime local naive."""
    return datetime.now(timezone.utc).astimezone(COLOMBIA_TZ).replace(tzinfo=None)


def format_datetime(value, fmt='%Y-%m-%d %H:%M'):
    """Formatea un datetime para mostrarlo en la zona horaria de Colombia."""
    if value is None:
        return ''
    if not isinstance(value, datetime):
        return str(value)
    if value.tzinfo is None:
        return value.strftime(fmt)
    return value.astimezone(COLOMBIA_TZ).strftime(fmt)
