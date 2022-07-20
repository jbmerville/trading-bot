
import pandas as pd

import os
import math
import random
import datetime
import time
import json
import enum
import sys
from Log_Functions import *
import Binance.BinanceFutureOrder as bi

from Phone_Notif import send_message


default_leverage = 25.0
default_tradingpair = "BTCUSDT"


class enum_Action(enum.Enum):
    nothing = 0
    order = 1
    manualtp = 2
    breakeven = 3
    uncertain = 4
    undefined = 404


class enum_OrderDirection(enum.Enum):
    buy = 0
    sell = 1


class Action_object:
    def __init__(self, content) -> None:
        self.content = content
        pass

    def display(self):
        return ""


class Order(Action_object):
    def __init__(self, direction: enum_OrderDirection, trading_pair, in_level, tp1_level, tp2_level, sl_level, leverage, content, posted_at) -> None:
        self.direction = direction
        self.tradingpair = trading_pair
        self.inlevel = in_level
        self.tp1level = tp1_level
        self.tp2level = tp2_level
        self.sllevel = sl_level
        self.leverage = leverage
        self.content = content
        self.posted_at = posted_at

    def display(self) -> str:
        res = "NEW ORDER SENT : "
        res = str(self.direction)+" + "+str(self.tradingpair)
        res = res+" +IN: "+str(self.inlevel)+" +LV: "+str(self.leverage)
        res = res+" +TP1 "+str(self.tp1level)+" +TP2: "+str(self.tp2level)
        res = res+" + SL: "+str(self.sllevel)
        return res


class Action:
    def __init__(self, action: enum_Action, action_obj: Action_object) -> None:
        self.actiontype = action
        self.action_obj = action_obj


class performAction(object):
    @staticmethod
    def hasToSendMessage(action: Action):
        send_message = False
        if (action.actiontype == enum_Action.order or action.actiontype == enum_Action.breakeven
                or action.actiontype == enum_Action.manualtp or action.actiontype == enum_Action.uncertain):
            send_message = True
        return send_message

    def getMessage(action: Action) -> str:
        message = ''
        if action.actiontype == enum_Action.breakeven:
            message = 'BE action: '+action.action_obj.content
        elif action.actiontype == enum_Action.manualtp:
            message = 'MANUAL TP action: '+action.action_obj.content
        elif action.actiontype == enum_Action.uncertain:
            message = 'UNCERTAINTY '+action.action_obj.content
        elif action.actiontype == enum_Action.order:
            message = 'ORDER '+action.action_obj.display() + ' Message: '+action.action_obj.content
        return message

    def messageAction(action: Action):
        if performAction.hasToSendMessage(action):
            message = performAction.getMessage(action)
            if not message == "":
                print("SENDING....")
                print(message)
                send_message(message)

    def orderAction(action: Action):
        if action.actiontype == enum_Action.order:
            bi.main_place_order(action.action_obj)

    def logSavingAction(action: Action, logfile: logFile):
        log = logObj(str(action.actiontype)+' TO DO '+action.action_obj.display() +
                     ' CONTENT '+action.action_obj.content, datetime.date.today())
        logfile.add_log(log)

    def performAction(action: Action):
        # order to do

        # log saving

        # send message
        performAction.messageAction(action)


class contentAnalyser(object):
    # to analyse the content "text" provided and determine what action to take
    @staticmethod
    def isManualTP(content: str):
        # to be called only if not order
        ManualTP = False

        if " tp " in content:
            if "ordre" in content or "ordonne" in content:
                ManualTP = True

        return ManualTP

    def isBreakEven(content):
        # to be called only if not order
        BE = False

        if "breakeven" in content:
            BE = True
        elif " be " in content:
            print(content)
        elif "be " in content and "sl " in content:
            BE = True

        return BE

    def isOrder(content) -> Order:

        trading_pair = None
        in_level = None
        direction = None
        tp1_level = None
        tp2_level = None
        sl_level = None
        lev_level = None
        order = None
        # direction
        has_direction, direction = contentAnalyser.hasDirection(content)
        if has_direction:
            has_pair, trading_pair = contentAnalyser.hasTradingPair(content)
            has_inlevel, in_level = contentAnalyser.hasInLevel(content, trading_pair)
            has_TP1, has_TP2, tp1_level, tp2_level = contentAnalyser.hasTP(content)
            has_SL, sl_level = contentAnalyser.hasSL(content)
            has_lev, lev_level = contentAnalyser.hasLeverage(content)
            if has_inlevel & has_TP1 & has_SL:
                is_OK = contentAnalyser.check_consistency(
                    direction, in_level, tp1_level, tp2_level, sl_level)
                if is_OK:
                    # it is an Order
                    if not has_lev:
                        lev_level = default_leverage  # default leverage
                    if not has_pair:
                        trading_pair = default_tradingpair  # default pair
                    order = Order(direction, trading_pair, in_level, tp1_level,
                                  tp2_level, sl_level, lev_level, content, None)
        return order

    def check_consistency(direction, in_val, tp1_val, tp2_val, sl_val):
        is_OK = False
        if direction == "SELL":
            if tp1_val < in_val:
                if sl_val > in_val:
                    if not tp2_val is None:
                        if tp2_val < in_val:
                            is_OK = True
                    else:
                        is_OK = True

        else:
            if tp1_val > in_val:
                if sl_val < in_val:
                    if not tp2_val is None:
                        if tp2_val > in_val:
                            is_OK = True
                    else:
                        is_OK = True

        return is_OK

    def hasDirection(content: str):
        has_direction = False
        direction = None

        if "buy" in content:
            has_direction = True
            direction = enum_OrderDirection.buy
        elif "sell" in content:
            has_direction = True
            direction = enum_OrderDirection.sell
        return has_direction, direction

    def hasTradingPair(content: str):
        has_pair = False
        trading_pair = None
        if "usdt" in content:
            has_pair = True
            content = content.split(" ")
            for s in content:
                if "usdt" in s:
                    trading_pair = s
                    break
        return has_pair, trading_pair

    def hasInLevel(content: str, trading_pair):
        has_inlevel = False
        in_level = None
        if not trading_pair is None:

            content = content.split(" ")
            index = content.index(trading_pair)
            value = content[index+1]+content[index+2]

            if "," in value:
                val = value.split(",")[0]
                digits = [int(s) for s in val.split() if s.isdigit()]
                value = ""

                for s in digits:
                    value = value+str(s)
                print(value)
                if value != "":
                    value = float(value)
                else:
                    value = 0

            else:
                digits = [int(s) for s in value.split() if s.isdigit()]
                value = ""

                for s in digits:
                    value = value+str(s)

                if value != "":
                    value = float(value)
                else:
                    value = 0
            if value > 0:
                in_level = value
                has_inlevel = True
        else:

            content = content.split(",")
            digits = [int(s) for s in content[0].split() if s.isdigit()]
            value = ""

            for s in digits:
                value = value+str(s)
            if value != "":
                value = float(value)
            else:
                value = 0
            if value > 0:
                in_level = value
                has_inlevel = True

        return has_inlevel, in_level

    def hasTP(content: str):
        has_TP1 = False
        has_TP2 = False
        tp1_level = None
        tp2_level = None
        if "tp2" in content:
            contenttp2 = content[content.find("tp2"):]
            contenttp2 = contenttp2.split(",")[0]
            value = ""
            prev_val_digit = False
            for s in contenttp2.split():

                if s.isdigit():
                    value = value+s
                    prev_val_digit = True

                elif prev_val_digit:
                    break
            if value != '':

                value = float(value)
            else:
                value = 0

            if value > 0:
                tp2_level = value
                has_TP2 = True

        if "tp1" in content:
            contenttp1 = content[content.find("tp1"):]
            contenttp1 = contenttp1.split(",")[0]
            value = ""
            prev_val_digit = False
            for s in contenttp1.split():

                if s.isdigit():
                    value = value+s
                    prev_val_digit = True

                elif prev_val_digit:
                    break
            if value != '':
                value = float(value)
            else:
                value = 0
            if value > 0:
                tp1_level = value
                has_TP1 = True
        elif "tp" in content:
            content = content[content.find("tp"):]
            content = content.split(",")[0]
            value = ""
            prev_val_digit = False
            for s in content.split():

                if s.isdigit():
                    value = value+s
                    prev_val_digit = True

                elif prev_val_digit:
                    break
            if value != '':
                value = float(value)
            else:
                value = 0
            if value > 0:
                tp1_level = value
                has_TP1 = True

        return has_TP1, has_TP2, tp1_level, tp2_level

    def hasSL(content: str):
        has_SL = False
        sl_level = None
        if "sl" in content:
            content = content[content.find("sl"):]
            content = content.split(",")[0]
            value = ""
            prev_val_digit = False
            for s in content.split():

                if s.isdigit():
                    value = value+s
                    prev_val_digit = True

                elif prev_val_digit:
                    break
            if value != '':
                value = float(value)
            else:
                value = 0
            if value > 0:
                sl_level = value
                has_SL = True
        return has_SL, sl_level

    def hasLeverage(content: str):
        has_lev = False
        leverage_level = None
        if "lev" in content:
            content = content[content.find("lev"):]
            content = content.split(",")[0]
            value = ""
            prev_val_digit = False
            for s in content.split():

                if s.isdigit():
                    value = value+s
                    prev_val_digit = True

                elif prev_val_digit:
                    break
            if value != "":
                value = float(value)
            else:
                value = 0
            if value > 0:
                leverage_level = value
                has_lev = True
        return has_lev, leverage_level

    def analysis(content) -> Action:

        action_to_do = Action(enum_Action.undefined, None)

        content = content.lower()
        # let's start checking if this is an order
        order = contentAnalyser.isOrder(content)
        if not order is None:
            print("ORDER FOUND")
            print(order.display())
            action_to_do = Action(enum_Action.order, order)
        else:
            isBE = contentAnalyser.isBreakEven(content)
            isManualTP = contentAnalyser.isManualTP(content)
            if isBE:
                if isManualTP:
                    # both
                    action_to_do = Action(enum_Action.breakeven, Action_object(content))
                else:
                    action_to_do = Action(enum_Action.breakeven, Action_object(content))
            else:
                if isManualTP:
                    action_to_do = Action(enum_Action.manualtp, Action_object(content))
                else:
                    action_to_do = Action(enum_Action.nothing, None)

        return action_to_do


def load_tweets_historic():
    tweets = pd.read_csv(os.path.expanduser("~//Desktop/tweets.csv"), index_col=0)
    return tweets


def backtest():
    tweets = load_tweets_historic()
    tweets.columns = ['content']
    c = 0
    for date_tweet in reversed(tweets.index):
        content = tweets.loc[date_tweet]['content']
        action = contentAnalyser.analysis(content)
        performAction.performAction(action)

    print(c)


def backtest_as_live():
    tweets = load_tweets_historic()
    tweets.columns = ['content']
    pos = 0
    tweets.index = pd.to_datetime(tweets.index)
    tweets = tweets.sort_index(ascending=True)
    # print(tweets.index[:10])
    random.seed('test')
    d_res = {}
    while pos < len(tweets.index):
        nb_tweets_new = random.randint(0, 10)
        # print(nb_tweets_new)
        end_pos = pos+nb_tweets_new
        if end_pos > len(tweets.index):
            end_pos = len(tweets.index)
        requested_tweets = tweets.iloc[range(pos, end_pos)]
        # print(requested_tweets)
        pos = end_pos
        requested_tweets = requested_tweets.to_dict()['content']
        # print(requested_tweets.keys())
        d = analysis(requested_tweets)
        d_res = {**d_res, **d}
    r = pd.DataFrame(index=d_res.keys(), columns=['content', 'decoded', 'TP1', 'TP2'])

    for res in d_res:

        r.loc[res]['content'] = d_res[res].content
        r.loc[res]['TP1'] = d_res[res].tp1level
        r.loc[res]['TP2'] = d_res[res].tp2level
        r.loc[res]['decoded'] = d_res[res].display()
    r.to_csv(os.path.expanduser("~//Desktop/Analysed_tweets.csv"))
    return


def test_mannually():
    d = {}
    d['2022-06-25 06:49:09+00:00'] = '🚨 SELL Btcusdt 21 285, tp 20 935, levier 25, SL 21 640 : dopaaa'
    d['2022-06-25 06:49:10+00:00'] = 'Tets'
    # setlasttimetweet(None)
    analysis(d)
    return


if __name__ == '__main__':
    # connect()
    backtest()

    # backtest_as_live()
    # live()
    # backtest_live()
    # test_mannually()

    print("Done")
