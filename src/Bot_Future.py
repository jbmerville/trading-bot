
from textwrap import indent
import pandas as pd
import tweepy
import os
import random
import datetime
import time
from dotenv import load_dotenv

lasttimetweet = None


class Order:
    def __init__(self, direction, trading_pair, in_level, tp1_level, tp2_level, sl_level, leverage, content, posted_at) -> None:
        self.direction = direction
        self.tradingpair = trading_pair
        self.inlevel = in_level
        self.tp1level = tp1_level
        self.tp2level = tp2_level
        self.sllevel = sl_level
        self.leverage = leverage
        self.content = content
        self.posted_at = posted_at

    def display(self):
        res = "NEW ORDER SENT : "
        res = self.direction+" + "+str(self.tradingpair)
        res = res+" +IN: "+str(self.inlevel)+" +LV: "+str(self.leverage)
        res = res+" +TP1 "+str(self.tp1level)+" +TP2: "+str(self.tp2level)
        res = res+" + SL: "+str(self.sllevel)
        return res


def get_historic():

    API_KEY = "63X3vA7dD5d20s3CL7ZYclces"
    API_SECRET = "8ns4qMr5Q4w9qk6VhKPP6UDmUeNRVfnTcjassP4IFUqteA3bMR"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAALN8eAEAAAAAkf3gFxC0Ew5ZiwDmneC79TDB01o%3DAbinG1C5PUjmaZE7YZrpg45ogVrssksgWEsEhcds9v65vqbKi1"
    ACCESS_TOKEN = "1387114169426747393-myEjHj9fbSPzbbbpogvy16mXGo3BwS"
    ACCESS_SECRET = "xc2o40E66ScoaaWv04jc3Ob9Lh6mVDkVZ2ACLcm2Hsu5d"
    # auth = tweepy.client(BEARER_TOKEN) #app only
    #auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    #auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # auth = tweepy.OAuth1UserHandler(
    #     consumer_key=API_KEY,
    #     consumer_secret=API_SECRET,
    #     access_token=ACCESS_TOKEN,
    #     access_token_secret=ACCESS_SECRET
    # )
    all_tweets = {}
    client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    #api = tweepy.API(auth)
    tweets = client.get_users_tweets(id="1210100315980210176", tweet_fields=[
                                     'text', 'created_at'], max_results=100)
    next_token = tweets.meta['next_token']
    for tweet in tweets.data:
        all_tweets[tweet.created_at] = tweet.text
    # other requests
    print(len(all_tweets))
    for i in range(0, 31):

        tweets = client.get_users_tweets(id="1210100315980210176", tweet_fields=[
                                         'text', 'created_at'], max_results=100, pagination_token=next_token)
        next_token = tweets.meta['next_token']
        for tweet in tweets.data:
            all_tweets[tweet.created_at] = tweet.text
        print(len(all_tweets))

    df = pd.DataFrame().from_dict(all_tweets, orient="index")
    df.to_csv(os.path.expanduser("~//Desktop/tweets.csv"))
    return all_tweets


def request_tweets():
    load_dotenv()
    API_KEY = os.getenv('TWITTER_API_KEY')
    API_SECRET = os.getenv('TWITTER_API_SECRET')
    BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
    # auth = tweepy.client(BEARER_TOKEN) #app only
    #auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    #auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # auth = tweepy.OAuth1UserHandler(
    #     consumer_key=API_KEY,
    #     consumer_secret=API_SECRET,
    #     access_token=ACCESS_TOKEN,
    #     access_token_secret=ACCESS_SECRET
    # )
    all_tweets = {}
    client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    #api = tweepy.API(auth)
    tweets = client.get_users_tweets(id="1210100315980210176", tweet_fields=[
                                     'text', 'created_at'], max_results=10)
    next_token = tweets.meta['next_token']
    for tweet in tweets.data:
        all_tweets[tweet.created_at] = tweet.text
    return all_tweets


def load_tweets_historic():
    tweets = pd.read_csv(os.path.expanduser("~//Desktop/tweets.csv"), index_col=0)
    return tweets


def isManualTP(content):
    # to be called only if not order
    ManualTP = False
    content = str(content)
    content = content.lower()
    if " tp " in content:
        if "ordre" in content:
            ManualTP = True

    return ManualTP


def isBreakEven(content):
    # to be called only if not order
    BE = False
    content = str(content)
    content = content.lower()
    if "breakeven" in content:
        BE = True
    elif " be " in content:
        print(content)

    return BE


def isOrder(content):
    is_Order = False
    trading_pair = None
    in_level = None
    direction = None
    tp1_level = None
    tp2_level = None
    sl_level = None
    lev_level = None

    content = str(content)
    content = content.lower()
    # direction
    has_direction, direction = hasDirection(content)
    # trading pair

    if has_direction:
        has_pair, trading_pair = hasTradingPair(content)
        has_inlevel, in_level = hasInLevel(content, trading_pair)
        has_TP1, has_TP2, tp1_level, tp2_level = hasTP(content)
        has_SL, sl_level = hasSL(content)
        has_lev, lev_level = hasLeverage(content)

        # print(content)
        # print("Direction: "+direction)
        # print("Pair "+ trading_pair)
        # print("IN: "+str(in_level))
        # print("SL "+str(sl_level))
        # print("LEV "+str(lev_level))
        if has_inlevel & has_TP1 & has_SL:
            # print("OK")
            is_OK = check_consistency(direction, in_level, tp1_level, tp2_level, sl_level)
            if is_OK:
                is_Order = True
                # print("ORDER OK !!")
                if not has_lev:
                    #print("NO LEVERAGE")
                    lev_level = 25.0  # default leverage
                if not has_pair:
                    trading_pair = "btcusdt"

                #print("ORDER NOT OK !!")
        else:

            print("NOT DECODED")

    return is_Order, trading_pair, direction, in_level, tp1_level, tp2_level, sl_level, lev_level


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
        direction = "BUY"
    elif "sell" in content:
        has_direction = True
        direction = "SELL"
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
            value = value.split(",")[0]
        try:
            value = float(value)
        except:
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
        value = float(value)

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
        value = float(value)
        if value > 0:
            leverage_level = value
            has_lev = True
    return has_lev, leverage_level


def backtest():
    tweets = load_tweets_historic()
    tweets.columns = ['content']
    c = 0
    for date_tweet in reversed(tweets.index):
        content = tweets.loc[date_tweet]['content']

        is_Order, trading_pair, direction, in_level, tp1_level, tp2_level, sl_level, lev_level = isOrder(
            content)
        if is_Order:
            c = c+1
            print(content)
            print("Direction: "+direction)
            print("Pair " + trading_pair)
            print("IN: "+str(in_level))
            print("TP1 "+str(tp1_level))
            print("TP2 "+str(tp2_level))
            print("SL "+str(sl_level))
            print("LEV "+str(lev_level))
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


def getlasttimetweet():
    return lasttimetweet


def setlasttimetweet(time):
    global lasttimetweet
    lasttimetweet = time
    return


def backtest_live():
    tweets = request_tweets()
    analysis(tweets)

    return


def analysis(dict_new_tweet):
    d_res = {}
    if getlasttimetweet() is None:
        days_1 = datetime.timedelta(1)
        setlasttimetweet(pd.to_datetime(list(dict_new_tweet.keys())[0])-days_1)
    for posted_at in dict_new_tweet.keys():
        posted_at_dt = pd.to_datetime(posted_at)
        # print(posted_at_dt)
        if posted_at_dt > getlasttimetweet():
            # alors on analysis=> new tweet
            setlasttimetweet(posted_at_dt)
            is_Order, trading_pair, direction, in_level, tp1_level, tp2_level, sl_level, lev_level = isOrder(
                dict_new_tweet[posted_at])
            if is_Order:
                # print("NEW ORDER DETECTED")
                # print("Direction: "+direction)
                # print("Pair " + trading_pair)
                # print("IN: "+str(in_level))
                # print("TP1 "+str(tp1_level))
                # print("TP2 "+str(tp2_level))
                # print("SL "+str(sl_level))
                # print("LEV "+str(lev_level))
                # print(posted_at)
                # print(dict_new_tweet[posted_at])
                o = Order(direction, trading_pair, in_level, tp1_level, tp2_level,
                          sl_level, lev_level, dict_new_tweet[posted_at], posted_at)
                d_res[posted_at] = o
                #print("ORDER TWEET : " + str(posted_at))
            else:
                # maybe manual TP
                isManualTP(dict_new_tweet[posted_at])
                isBreakEven(dict_new_tweet[posted_at])

    return d_res


def test_mannually():
    d = {}
    d['2022-06-25 06:49:09+00:00'] = '🚨 SELL Btcusdt 21 285, tp 20 935, levier 25, SL 21 640 : dopaaa'
    d['2022-06-25 06:49:10+00:00'] = 'Tets'
    # setlasttimetweet(None)
    analysis(d)
    return


def live():
    lasttimetweet = None
    nb_request = 0

    while True:
        nb_request = nb_request+1
        print(nb_request)
        all_tweets = request_tweets()
        d_order = analysis(all_tweets)
        if len(d_order) > 0:
            for o in d_order:
                print(d_order[o].display())
        time.sleep(30)

    return


if __name__ == '__main__':
    # connect()
    # backtest()

    backtest_as_live()
    # live()
    # backtest_live()
    # test_mannually()

    print("Done")
