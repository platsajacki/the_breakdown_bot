import pytest

from tests.factory import FixtureFactory


@pytest.fixture
def level_data(factory: FixtureFactory) -> dict:
    schema = factory.schema(
        schema=lambda: {
            'ticker': factory.field('cryptocurrency_iso_code'),
            'level': factory.price,
            'round_price': factory.field('random.randint', a=1, b=8),
        },
        iterations=1,
    )
    return schema.create()[0]
