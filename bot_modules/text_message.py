from dataclasses import dataclass

from constants import COIN, MONEY_BAG, MONEY_WITH_WINGS, ROCKET


@dataclass
class InfoMessage:
    """The class contains message templates."""
    WALLET_MASSAGE: str = f'_______{MONEY_BAG}_______' + '''
Equity - {equity};
Unrealised PNL - {unreal_pnl};
Balance - {balance};
Realised PNL - {real_pnl}.'''

    OPEN_ORDER_MESSAGE: str = '''The order was opened!
''' + f'{MONEY_WITH_WINGS} ' + '''{symbol}:
Asset volume - {asset_volume};
Trigger - {trigger};
Entry point - {entry_point};
Stop-loss - {stop_loss};
Take-profit - {take_profit}.'''

    ORDER_MESSAGE: str = f'{MONEY_WITH_WINGS} ' + '''{symbol}:
Side - {side};
Entry point - {price};
Asset volume - {qty};
Trigger - {triggerPrice};
Stop-loss - {stopLoss};
Take-profit - {takeProfit}.'''

    ORDER_TP_SL_MESSAGE: str = f'{MONEY_WITH_WINGS} ' + '''{symbol}:
Side - {side};
Asset volume - {qty};
Trigger - {triggerPrice};
Order type - {orderType}.'''

    POSITION_MESSAGE: str = f'{COIN} ' + '''{symbol}:
Side - {side};
Asset volume - {size};
Leverage - {leverage};
Entry point - {avgPrice};
Marking price - {markPrice};
Unrealised PNL - {unrealisedPnl};
Stop-loss - {stopLoss};
Trailing stop - {trailingStop};
Take-profit - {takeProfit}.'''

    TRADE_MESSAGE: str = f'{ROCKET} ' + '''{symbol}:
Side - {side};
Asset volume - {execQty};
Price - {execPrice}.'''

    QUERY_LIMIT: str = '''{ticker} - {trend}:
LVL - {level};
Create - {create}.'''
