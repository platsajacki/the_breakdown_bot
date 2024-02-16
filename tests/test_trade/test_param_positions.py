import pytest

from trade.param_position import Long, Position, Short


def test_calculate_stop(level_data: dict):
    assert Position(**level_data).calculate_stop() == Position.COEF_STOP * level_data['level']


def test_calculate_luft(level_data: dict):
    position = Position(**level_data)
    assert position.calculate_luft() == Position.COEF_LUFT * position.calculate_stop()


def test_long_get_param_position(level_data: dict):
    long = Long(**level_data)
    long_param = long.get_param_position()
    entry_point = round(level_data['level'] + long.calculate_luft(), level_data['round_price'])
    assert long_param[0] == level_data['ticker']
    assert long_param[1] == entry_point
    assert long_param[2] == round(entry_point - long.calculate_stop(), level_data['round_price'])
    assert long_param[3] == round(entry_point + long.COEF_PROFIT * long.calculate_stop(), level_data['round_price'])
    assert long_param[4] == round(entry_point * long.COEF_TRIGGER_LONG, level_data['round_price'])


def test_short_get_param_position(level_data: dict):
    short = Short(**level_data)
    short_param = short.get_param_position()
    entry_point = round(level_data['level'] - short.calculate_luft(), level_data['round_price'])
    assert short_param[0] == level_data['ticker']
    assert short_param[1] == entry_point
    assert short_param[2] == round(entry_point + short.calculate_stop(), level_data['round_price'])
    assert short_param[3] == round(entry_point - short.COEF_PROFIT * short.calculate_stop(), level_data['round_price'])
    assert short_param[4] == round(entry_point * short.COEF_TRIGGER_SHORT, level_data['round_price'])


@pytest.mark.parametrize('position', (Long, Short))
def test_long_and_short_get_trailing_stop_param(position: Long | Short, level_data: dict):
    pos = position(**level_data)  # type: ignore[operator]
    entry_point = pos.get_param_position()[1]
    trailing_stop_param = Long.get_trailing_stop_param(entry_point, level_data['round_price'])
    assert trailing_stop_param[0] == pos.get_trailing_stop(entry_point, level_data['round_price'])
    assert trailing_stop_param[1] == round(
        entry_point + entry_point * pos.COEF_ACTIVE_PRICE, level_data['round_price']
    )
