import unittest
from unittest.mock import MagicMock
from src.binance.binance_future_order import BinanceFutureOrder
from src.binance.binance_client_wrapper import BinanceClientWrapper

PERCENTAGE_TO_INVEST = 33
TRADING_PAIR = 'BTCUSDT'
DIRECTION = 'BUY'
ENTRY_PRICE = 0
ORDER_TYPE = 'LIMIT'
LEVERAGE = ''
STOP_LOSS_PRICE = 0
TAKE_PROFIT_PRICE = 0
AMOUNT = 0


class BBinanceClientWrapperTest(unittest.TestCase):
    def test_init(self):
        # Arrange
        binance_client_wrapper = BinanceClientWrapper()

        # Assert
        self.assertTrue(binance_client_wrapper.available_trading_pairs, ['BTCUSDT', 'EGLDUSDT'])

    def test_get_trading_pair_price(self):
        # Arrange
        binance_client_wrapper = BinanceClientWrapper()
        input = 'trading_pair'
        expected = '1.0'
        binance_client_wrapper.client.futures_symbol_ticker = MagicMock(
            input, return_value={'price': expected})

        # Act
        result = binance_client_wrapper.get_trading_pair_price(input)

        # Assert
        self.assertTrue(result, float(expected))

    def test_get_trading_pair_price(self):
        # Arrange
        binance_client_wrapper = BinanceClientWrapper()
        binance_client_wrapper.client.futures_symbol_ticker = MagicMock(
            TRADING_PAIR, return_value={'price': '11.0'})

        # Act
        result = binance_client_wrapper.get_trading_pair_price(TRADING_PAIR)

        # Assert
        self.assertTrue(result, 11.0)

    def test_should_execute_order_true(self):
        # Arrange
        binance_client_wrapper = BinanceClientWrapper()
        binance_future_order = self.create_dummy_binance_future_order()
        binance_future_order.entry_price = 10.0
        binance_client_wrapper.get_trading_pair_price = MagicMock(
            input, return_value=11.0)

        # Act
        result = binance_client_wrapper.should_execute_order(binance_future_order)

        # Assert
        self.assertTrue(result)

    def test_should_execute_order_false(self):
        # Arrange
        binance_client_wrapper = BinanceClientWrapper()
        binance_future_order = self.create_dummy_binance_future_order()
        binance_future_order.entry_price = 10.0
        binance_client_wrapper.get_trading_pair_price = MagicMock(
            input, return_value=13.0)

        # Act
        result = binance_client_wrapper.should_execute_order(binance_future_order)

        # Assert
        self.assertFalse(result)

    def test_submit_future_order(self):
        # Arrange
        binance_client_wrapper = BinanceClientWrapper()
        binance_future_order = self.create_dummy_binance_future_order()
        binance_client_wrapper.should_execute_order = MagicMock(
            return_value=True)
        binance_client_wrapper.client.create_test_order = MagicMock(
            return_value=None)

        # Act
        result = binance_client_wrapper.submit_future_order(binance_future_order)

        # Assert
        self.assertEqual(result, None)

    def create_dummy_binance_future_order(self):
        return BinanceFutureOrder(PERCENTAGE_TO_INVEST, TRADING_PAIR, DIRECTION, ENTRY_PRICE,
                                  ORDER_TYPE, LEVERAGE, STOP_LOSS_PRICE, TAKE_PROFIT_PRICE, AMOUNT)
