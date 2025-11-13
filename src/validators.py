"""Validadores y sanitizadores para entrada de datos."""
import re
from typing import Optional, Union


def sanitize_string(value: str, max_length: int = 200) -> str:
    """
    Sanitiza una cadena eliminando caracteres peligrosos.

    Args:
        value: Cadena a sanitizar
        max_length: Longitud máxima permitida

    Returns:
        Cadena sanitizada
    """
    if not isinstance(value, str):
        raise ValueError("El valor debe ser una cadena")

    # Eliminar espacios en blanco al inicio y al final
    value = value.strip()

    # Limitar longitud
    if len(value) > max_length:
        value = value[:max_length]

    # Eliminar caracteres de control y caracteres peligrosos
    value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)

    return value


def validate_email(email: str) -> bool:
    """
    Valida formato de email.

    Args:
        email: Email a validar

    Returns:
        True si el email es válido
    """
    if not email or not isinstance(email, str):
        return False

    # Patrón básico de validación de email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Valida formato de teléfono.

    Args:
        phone: Teléfono a validar

    Returns:
        True si el teléfono es válido
    """
    if not phone or not isinstance(phone, str):
        return False

    # Eliminar espacios, guiones y paréntesis
    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)

    # Verificar que solo contenga dígitos y tenga longitud razonable
    return phone_clean.isdigit() and 7 <= len(phone_clean) <= 15


def validate_positive_integer(value: Union[str, int], min_value: int = 0) -> Optional[int]:
    """
    Valida y convierte un entero positivo.

    Args:
        value: Valor a validar
        min_value: Valor mínimo permitido

    Returns:
        Entero validado o None si es inválido
    """
    try:
        int_value = int(value)
        if int_value >= min_value:
            return int_value
    except (ValueError, TypeError):
        pass
    return None


def validate_positive_float(value: Union[str, float], min_value: float = 0.0) -> Optional[float]:
    """
    Valida y convierte un número decimal positivo.

    Args:
        value: Valor a validar
        min_value: Valor mínimo permitido

    Returns:
        Float validado o None si es inválido
    """
    try:
        float_value = float(value)
        if float_value >= min_value:
            return float_value
    except (ValueError, TypeError):
        pass
    return None


def validate_date_string(date_str: str) -> bool:
    """
    Valida formato de fecha YYYY-MM-DD.

    Args:
        date_str: Cadena de fecha a validar

    Returns:
        True si el formato es válido
    """
    if not date_str or not isinstance(date_str, str):
        return False

    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_str))


def validate_estado(estado: str, valid_estados: list) -> bool:
    """
    Valida que el estado esté en una lista de valores permitidos.

    Args:
        estado: Estado a validar
        valid_estados: Lista de estados válidos

    Returns:
        True si el estado es válido
    """
    if not estado or not isinstance(estado, str):
        return False

    return estado.lower() in [e.lower() for e in valid_estados]
