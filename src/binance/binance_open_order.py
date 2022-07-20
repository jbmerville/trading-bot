import json
import os


class BinanceOpenOrder():
    def __init__(self, order_id, trading_pair, type, executed_quantity, side, time):
        if trading_pair not in list(os.getenv('BINANCE_AVAILABLE_TRADING_PAIR').split(",")):
            raise Exception(
                f'trading_pair should be either of {list(os.getenv("BINANCE_AVAILABLE_TRADING_PAIR").split(","))}, was {trading_pair}')
        self.order_id = order_id
        self.trading_pair = trading_pair
        self.type = type
        self.executed_quantity = executed_quantity
        self.side = side
        self.time = time

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)
