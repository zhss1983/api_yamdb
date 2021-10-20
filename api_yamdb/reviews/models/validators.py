from django.utils.timezone import now
from django.core.exceptions import ValidationError

def year_validator(value):
    if value > now().year:
        raise ValidationError(
            f'Не корректное значение поля year: {value}!')
