from decimal import Decimal


def check_and_get_value(message) -> Decimal:
    """Conversion of the entered value to Decimal."""
    value_str: str = message.text
    if ',' in value_str:
        value_str = value_str.replace(',', '.')
    return Decimal(value_str)
