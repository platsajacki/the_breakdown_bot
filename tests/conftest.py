import pytest

from tests.factory import FixtureFactory

pytest_plugins = [
    'tests.fixtures.levels'
]


@pytest.fixture
def factory() -> FixtureFactory:
    return FixtureFactory()
