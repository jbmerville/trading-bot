import json
import os


class BinanceFutureOrder():
    def __init__(self, percentage_to_invest, trading_pair, direction, entry_price, order_type, leverage, stop_loss_price, take_profit_price, amount):
        if direction not in ['BUY', 'SELL']:
            raise Exception(f'direction should be either BUY or SELL, was {direction}')
        if order_type not in ['LIMIT']:
            raise Exception(f'order_type should be LIMIT, was {order_type}')
        if trading_pair not in list(os.getenv('BINANCE_AVAILABLE_TRADING_PAIR').split(",")):
            raise Exception(
                f'trading_pair should be either of {list(os.getenv("BINANCE_AVAILABLE_TRADING_PAIR").split(","))}, was {trading_pair}')
        self.percentage_to_invest = percentage_to_invest
        self.trading_pair = trading_pair
        self.direction = direction
        self.entry_price = entry_price
        self.order_type = order_type
        self.leverage = leverage
        self.stop_loss_price = stop_loss_price
        self.take_profit_price = take_profit_price
        self.amount = amount

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)
