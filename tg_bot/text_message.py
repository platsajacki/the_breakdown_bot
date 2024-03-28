from dataclasses import dataclass
from decimal import Decimal

from settings.constants import COIN, MONEY_BAG, MONEY_WITH_WINGS, POWER_RESERVE_USED_UP, ROCKET


@dataclass
class InfoMessage:
    """The class contains message templates."""
    WALLET_MASSAGE: str = f'_____________{MONEY_BAG}_____________' + '''
Equity - <b>{equity}</b>
Unrealised PNL - <b>{unreal_pnl}</b>
Balance - <b>{balance}</b>
Realised PNL - <b>{real_pnl}</b>'''

    OPEN_ORDER_MESSAGE: str = '''<b>The order was opened!</b>
''' + f'{MONEY_WITH_WINGS} ' + '''<b>{symbol}</b>
Asset volume - <b>{asset_volume}</b>
Trigger - <b>{trigger}</b>
Entry point - <b>{entry_point}</b>
Stop-loss - <b>{stop_loss}</b>
Take-profit - <b>{take_profit}</b>'''

    ORDER_MESSAGE: str = f'{MONEY_WITH_WINGS} ' + '''<b>{symbol}</b>
Side - <b>{side}</b>
Entry point - <b>{price}</b>
Asset volume - <b>{qty}</b>
Trigger - <b>{triggerPrice}</b>
Stop-loss - <b>{stopLoss}</b>
Take-profit - <b>{takeProfit}</b>'''

    ORDER_TP_SL_MESSAGE: str = f'{MONEY_WITH_WINGS} ' + '''<b>{symbol}</b>
Side - <b>{side}</b>
Asset volume - <b>{qty}</b>
Trigger - <b>{triggerPrice}</b>
Order type - <b>{orderType}</b>'''

    POSITION_MESSAGE: str = f'{COIN} ' + '''<b>{symbol}</b>
Side - <b>{side}</b>
Asset volume - <b>{size}</b>
Leverage - <b>{leverage}</b>
Entry point - <b>{avgPrice}</b>
Marking price - <b>{markPrice}</b>
Unrealised PNL - <b>{unrealisedPnl}</b>
Stop-loss - <b>{stopLoss}</b>
Trailing stop - <b>{trailingStop}</b>
Take-profit - <b>{takeProfit}</b>'''

    TRADE_MESSAGE: str = f'{ROCKET} ' + '''<b>{symbol}</b>
Side - <b>{side}</b>
Asset volume - <b>{execQty}</b>
Price - <b>{execPrice}</b>'''

    QUERY_LIMIT: str = '''<b>{ticker} - {trend}</b>
LVL - <b>{level}</b>
Create - <b>{create}</b>'''

    @staticmethod
    def get_text_not_worked_out_level(
        ticker: str, level: Decimal, current_price_movement: Decimal | None, median_price: Decimal | None
    ) -> str:
        avg_info = (
            f'\n<b>{median_price * POWER_RESERVE_USED_UP} &lt {current_price_movement}</b>'
            if median_price and current_price_movement else
            'The price crossed the level earlier.'
        )
        return f'The <b>`{ticker} - {level}`</b> level has not worked out.{avg_info}'
