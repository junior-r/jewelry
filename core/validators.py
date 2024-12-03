from django.core.exceptions import ValidationError


def small_file_size_validator(value):
    limit = 1 * 1024 * 1024  # 1MB
    if value.size > limit:
        raise ValidationError('Archivo demasiado grande. El tamaño máximo permitido es de 1MB.')


def big_file_size_validator(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Archivo demasiado grande. El tamaño máximo permitido es de 5MB.')
