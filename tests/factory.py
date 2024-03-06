from decimal import Decimal
from random import randint

from mimesis import Field, Fieldset, Generic, Schema
from mimesis.locales import Locale

from settings.constants import USDT

generic = Generic(locale=Locale.EN)
field = Field(locale=Locale.EN)
fieldset = Fieldset(locale=Locale.EN)


class FixtureFactory:
    def __init__(self) -> None:
        self.generic = generic
        self.field = field
        self.fieldset = fieldset
        self.schema = Schema

    @property
    def symbol(self) -> str:
        return self.field('cryptocurrency_iso_code') + USDT

    @property
    def price(self) -> Decimal:
        return round(self.field('decimal_number', start=0.00000001, end=100000.0), randint(0, 8))
