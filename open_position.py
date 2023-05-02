from pybit.unified_trading import HTTP
import keys

session = HTTP(
    testnet=True,
    api_key=keys.api_key,
    api_secret=keys.api_secret)

session.place_order(
    category="inverse",
    symbol="BTCUSDT",
    side="Buy",
    orderType="Limit",
    qty="0.05",
    tryggeBy='MarkPrice',
    triggerDirection=1,
    triggerPrice='35400',
    price="30600",
    takeProfit='30880',
    stopLoss='29999',
    orderFilter="Order")
