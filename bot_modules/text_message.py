WALLET_MASSAGE = '''Equity - {equity};
Unrealised PNL - {unreal_pnl};
Balance - {balance};
Realised PNL - {real_pnl}.'''

OPEN_ORDER_MESSAGE = '''The order was opened - {symbol};
Asset volume - {asset_volume}
Trigger - {trigger};
Entry point - {entry_point};
Stop-loss - {stop_loss};
Take-profit - {take_profit}.'''

ORDER_MESSAGE = '''{symbol}:
Side - {side};
Entry point - {entry_point};
Asset volume - {qty}:
Trigger - {trigger_price};
Stop-loss - {stop_loss};
Take-profit - {take_profit}.'''

ORDER_TP_SL_MESSAGE = '''{symbol}:
Side - {side};
Asset volume - {qty};
Trigger - {trigger_price};
Order type - {order_type}.'''

POSITION_MESSAGE = '''{symbol}:
Side - {side};
Asset volume - {size};
Leverage - {leverage};
Entry point - {avg_price};
Unrealised PNL - {unrealised_pnl};
Stop-loss - {stop_loss};
Take-profit - {take_profit}.'''
