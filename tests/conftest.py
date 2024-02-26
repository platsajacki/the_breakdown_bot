import pytest

from tests.factory import FixtureFactory

pytest_plugins = [
    'tests.fixtures.levels',
    'tests.fixtures.messages_for_callback',
]


@pytest.fixture
def factory() -> FixtureFactory:
    return FixtureFactory()
