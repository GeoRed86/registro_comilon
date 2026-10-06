import re
from django.core.exceptions import ValidationError

def validar_rut(valor):
    
    patron = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
    if not re.match(patron, valor):
        raise ValidationError('El RUT debe tener el formato 12.345.678-9 o 1.234.567-K')