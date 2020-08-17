import requests
import json
from config import *
import asyncio
import copy
import datetime
import sys
import alpaca_trade_api as tradeapi


def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)


def print_pretty(object):
    print(json.dumps(object, indent=2, sort_keys=True))


def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(r.content)


def get_all_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)
    return json.loads(r.content)


def get_order(symbol):
    orders = get_all_orders()
    for asset in orders:
        if(asset['symbol'] == symbol):
            return asset


def get_positions():
    r = requests.get(POSITIONS_URL, headers=HEADERS)
    return json.loads(r.content)


def liquidate_gains():
    try:
        assets = get_positions()
        for position in assets:
            # print(1)
            if(float(position['unrealized_pl']) >= (SELL_MARGIN * RISK) and get_order(position['symbol']) is None):
                # print(2)
                if(float(position['qty']) > 0 and get_order(position['symbol']) is None):
                    # print(3)
                    create_order(
                        position['symbol'], position['qty'], "sell", "market", "ioc")
                else:
                    create_order(
                        position['symbol'], str(-1 * int(position['qty'])), "buy", "market", "ioc")
                sell = float(position['current_price'])
                print("Sell {} at {}".format(position['symbol'], sell))
    except:
        e = sys.exc_info()[0]
        print("{} in liquidate_gains()".format(e))
        sys.exit(1)


def purchase_at_low():
    positions = get_positions()
    interests = copy.deepcopy(STOCKS)
    for item in positions:
        if item['symbol'] in interests:
            interests.remove(item['symbol'])
    for item in interests:
        if(get_order(item) is None and buy_parameter_1(item)):
            r = create_order(item, int(RISK), "buy", "market", "ioc")
            print("Buy {}".format(item))

# takes in the symbol and lim=number of bars to return


def get_bars(symbols, lim=2):
    api = tradeapi.REST(API_KEY, SECRET_KEY,
                        BASE_URL_ACCOUNT, api_version='v2')

    # Get daily price data for AAPL over the last 5 trading days.
    barset = api.get_barset(symbols, 'day', limit=lim)
    bars = barset[symbols]
    # for i in range(0, len(bars)):
    #     print("high: {} low: {} close: {}".format(
    #         bars[i].h, bars[i].l, bars[i].c))

    return bars

# is the last bid_price within 20% of the last minute bar low, if so buy


def buy_parameter_1(symbol):
    quote = get_last_quote(symbol)
    bars = get_bars(symbol)
    thresh = (float(bars[0].h) - float(bars[0].l)
              ) * .2 + float(bars[0].l)
    if(quote["last"]["bidprice"] < thresh and float(bars[1].l) < float(bars[0].l)):
        # print("BUY {}".format(symbol))
        return True
    return False
    # print("{} at {} with thresh {}".format(
    #     symbol, quote["last"]["bidprice"], thresh))

    return False


def get_last_trade(symbol):
    r = requests.get(
        "{}/{}".format(POSITIONS_URL, symbol), headers=HEADERS)
    return json.loads(r.content)


def get_last_quote(symbol):
    r = requests.get("{}{}".format(QUOTE_URL, symbol), headers=HEADERS)
    return json.loads(r.content)


def main():
    while(True):
        liquidate_gains()
        # purchase_at_low()


if __name__ == "__main__":
    main()
