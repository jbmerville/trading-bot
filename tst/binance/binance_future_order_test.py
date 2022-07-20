import unittest

from src.binance.binance_future_order import BinanceFutureOrder

PERCENTAGE_TO_INVEST = 33
TRADING_PAIR = 'BTCUSDT'
DIRECTION = 'BUY'
ENTRY_PRICE = 0
ORDER_TYPE = 'LIMIT'
LEVERAGE = ''
STOP_LOSS_PRICE = 0
TAKE_PROFIT_PRICE = 0
AMOUNT = 0


class BinanceFutureOrderTest(unittest.TestCase):
    def test_init_valid(self):
        # Arrange
        binance_future_order = BinanceFutureOrder(PERCENTAGE_TO_INVEST, TRADING_PAIR, DIRECTION, ENTRY_PRICE,
                                                  ORDER_TYPE, LEVERAGE, STOP_LOSS_PRICE, TAKE_PROFIT_PRICE, AMOUNT)

        # Assert
        self.assertEqual(PERCENTAGE_TO_INVEST, binance_future_order.percentage_to_invest)
        self.assertEqual(TRADING_PAIR, binance_future_order.trading_pair)
        self.assertEqual(DIRECTION, binance_future_order.direction)
        self.assertEqual(ENTRY_PRICE, binance_future_order.entry_price)
        self.assertEqual(ORDER_TYPE, binance_future_order.order_type)
        self.assertEqual(LEVERAGE, binance_future_order.leverage)
        self.assertEqual(STOP_LOSS_PRICE, binance_future_order.stop_loss_price)
        self.assertEqual(TAKE_PROFIT_PRICE, binance_future_order.take_profit_price)
        self.assertEqual(AMOUNT, binance_future_order.amount)

    def test_init_invalid_direction_expection(self):
        # Arrange
        direction = 'invalid_direction'

        # Assert
        self.assertRaises(Exception,
                          BinanceFutureOrder, (PERCENTAGE_TO_INVEST, TRADING_PAIR, direction, ENTRY_PRICE,
                                               ORDER_TYPE, LEVERAGE, STOP_LOSS_PRICE, TAKE_PROFIT_PRICE, AMOUNT))

    def test_init_invalid_order_type_expection(self):
        # Arrange
        order_type = 'invalid_order_type'

        # Assert
        self.assertRaises(Exception,
                          BinanceFutureOrder, (PERCENTAGE_TO_INVEST, TRADING_PAIR, DIRECTION, ENTRY_PRICE,
                                               order_type, LEVERAGE, STOP_LOSS_PRICE, TAKE_PROFIT_PRICE, AMOUNT))

    def test_init_invalid_trading_pair_expection(self):
        # Arrange
        trading_pair = 'invalid_trading_pair'

        # Assert
        self.assertRaises(Exception,
                          BinanceFutureOrder, (PERCENTAGE_TO_INVEST, trading_pair, DIRECTION, ENTRY_PRICE,
                                               ORDER_TYPE, LEVERAGE, STOP_LOSS_PRICE, TAKE_PROFIT_PRICE, AMOUNT))

    def test_display(self):
        # Arrange
        binance_future_order = BinanceFutureOrder(PERCENTAGE_TO_INVEST, TRADING_PAIR, DIRECTION, ENTRY_PRICE,
                                                  ORDER_TYPE, LEVERAGE, STOP_LOSS_PRICE, TAKE_PROFIT_PRICE, AMOUNT)

        # Assert
        self.assertEqual('{\n  "percentage_to_invest": 33,\n  "trading_pair": "BTCUSDT",\n  "direction": "BUY",\n  "entry_price": 0,\n  "order_type": "LIMIT",\n  "leverage": "",\n  "stop_loss_price": 0,\n  "take_profit_price": 0,\n  "amount": 0\n}', binance_future_order.__str__(
        ))
