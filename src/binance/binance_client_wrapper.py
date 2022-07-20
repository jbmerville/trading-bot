from binance.client import Client
import os
import logging

from src.binance.binance_future_order import BinanceFutureOrder


class BinanceClientWrapper():
    def __init__(self):
        API_KEY = os.getenv('BINANCE_API_KEY')
        SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
        self.client = Client(API_KEY, SECRET_KEY, testnet=False)
        self.available_trading_pairs = list(os.getenv('BINANCE_AVAILABLE_TRADING_PAIR').split(","))

    def get_trading_pair_price(self, trading_pair):
        res = self.client.futures_symbol_ticker(symbol=trading_pair)
        price = float(res['price'])
        logging.info(f'Current price for trading pair: {trading_pair} is {price}')
        return price

    def submit_future_order(self, binance_future_order: BinanceFutureOrder):
        if type(binance_future_order) != BinanceFutureOrder:
            raise Exception(
                f'binance_future_order should be of type BinanceFutureOrder, was {type(binance_future_order)}')
        if not self.should_execute_order():
            raise Exception(
                f'Order entry price was too far from the current trading pair {binance_future_order.trading_pair} price')
        res = self.client.create_test_order(
            symbol=binance_future_order.trading_pair,
            type=binance_future_order.order_type,
            timeInForce='GTC',
            side=binance_future_order.direction,
            quantity=binance_future_order.amount,
            price=binance_future_order.entry_price)
        logging.info(res)

    def should_execute_order(self, binance_future_order: BinanceFutureOrder):
        """Check to see if the entry price found in the order is not too far from the current price """

        if type(binance_future_order) != BinanceFutureOrder:
            raise Exception(
                f'binance_future_order should be of type BinanceFutureOrder, was {type(binance_future_order)}')
        current_price = self.get_trading_pair_price(binance_future_order.trading_pair)
        price_difference_ratio = current_price / binance_future_order.entry_price
        logging.info(
            f'Price difference for order with trading pair: {binance_future_order.trading_pair} is {price_difference_ratio}')
        return price_difference_ratio < 1.2 and price_difference_ratio > 0.8
