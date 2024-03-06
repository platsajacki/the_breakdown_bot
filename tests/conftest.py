import pytest

from tests.factory import FixtureFactory

pytest_plugins = [
    'tests.fixtures.levels',
    'tests.fixtures.messages_for_callback',
    'tests.fixtures.mocks',
]


@pytest.fixture
def factory() -> FixtureFactory:
    return FixtureFactory()
