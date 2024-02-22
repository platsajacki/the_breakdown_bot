from mimesis import Field, Fieldset, Generic, Schema
from mimesis.locales import Locale

generic = Generic(locale=Locale.EN)
field = Field(locale=Locale.EN)
fieldset = Fieldset(locale=Locale.EN)


class FixtureFactory:
    def __init__(self) -> None:
        self.generic = generic
        self.field = field
        self.fieldset = fieldset
        self.schema = Schema
