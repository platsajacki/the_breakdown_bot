from dataclasses import dataclass


@dataclass
class InfoMessage:
    WALLET_MASSAGE: str = '''Equity - {equity};
Unrealised PNL - {unreal_pnl};
Balance - {balance};
Realised PNL - {real_pnl}.'''

    OPEN_ORDER_MESSAGE: str = '''The order was opened!
{smile}{symbol}{smile}
Asset volume - {asset_volume};
Trigger - {trigger};
Entry point - {entry_point};
Stop-loss - {stop_loss};
Take-profit - {take_profit}.'''

    ORDER_MESSAGE: str = '''{symbol}:
Side - {side};
Entry point - {entry_point};
Asset volume - {qty};
Trigger - {trigger_price};
Stop-loss - {stop_loss};
Take-profit - {take_profit}.'''

    ORDER_TP_SL_MESSAGE: str = '''{symbol}:
Side - {side};
Asset volume - {qty};
Trigger - {trigger_price};
Order type - {order_type}.'''

    POSITION_MESSAGE: str = '''{symbol}:
Side - {side};
Asset volume - {size};
Leverage - {leverage};
Entry point - {avg_price};
Marking price - {mark_price};
Unrealised PNL - {unrealised_pnl};
Stop-loss - {stop_loss};
Take-profit - {take_profit}.'''

    QUERY_LIMIT: str = '''{ticker} - {trend}
LVL - {level}
Create - {create}
'''
