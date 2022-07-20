import unittest

from src.binance.binance_open_order import BinanceOpenOrder
ORDER_ID = 3058874418
TRADING_PAIR = 'BTCUSDT'
TYPE = 'TAKE_PROFIT_MARKET'
EXECUTED_QUANTITY = '0'
SIDE = 'BOTH'
TIME = '1657174292714'


class BinanceOpenOrderTest(unittest.TestCase):
    def test_init_valid(self):
        # Arrange
        binance_open_order = BinanceOpenOrder(ORDER_ID, TRADING_PAIR, TYPE, EXECUTED_QUANTITY, SIDE, TIME)

        # Assert
        self.assertEqual(ORDER_ID, binance_open_order.order_id)
        self.assertEqual(TRADING_PAIR, binance_open_order.trading_pair)
        self.assertEqual(TYPE, binance_open_order.executed_quantity)
        self.assertEqual(SIDE, binance_open_order.side)
        self.assertEqual(TIME, binance_open_order.time)

    def test_init_invalid_order_id_exception(self):
        # Arrange
        order_id = 'invalid_order_id'

        # Assert
        self.assertRaises(Exception, BinanceOpenOrder, (order_id, TRADING_PAIR, TYPE, EXECUTED_QUANTITY, SIDE, TIME))

    def test_init_invalid_trading_pair_expection(self):
        # Arrange
        trading_pair = 'invalid_trading_pair'

        # Assert
        self.assertRaises(Exception,
                          BinanceOpenOrder, (ORDER_ID, trading_pair, TYPE, EXECUTED_QUANTITY, SIDE, TIME))

    def test_init_invalid_type_expection(self):
        # Arrange
        type = 'invalid_type'

        # Assert
        self.assertRaises(Exception,
                          BinanceOpenOrder, (ORDER_ID, TRADING_PAIR, type, EXECUTED_QUANTITY, SIDE, TIME))

    def test_display(self):
        # Arrange
        binance_open_order = BinanceOpenOrder(ORDER_ID, TRADING_PAIR, TYPE, EXECUTED_QUANTITY, SIDE, TIME)

        # Assert
        self.assertEqual('{\n  "order_id": 3058874418,\n  "trading_pair": "BTCUSDT",\n  "type": "TAKE_PROFIT_MARKET",\n  "executed_quantity": "0",\n  "side": "BOTH",\n  "time": "1657174292714"\n}', binance_open_order.__str__(
        ))
