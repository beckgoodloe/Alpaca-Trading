import websocket
import json
import asyncio
from config import *
import trade

trade_data = {}


def print_pretty(object):
    print(json.dumps(object, indent=2, sort_keys=True))


def on_open(ws):
    auth_data = {"action": "authenticate", "data": {
        "key_id": API_KEY, "secret_key": SECRET_KEY}}
    ws.send(json.dumps(auth_data))

    stocks_of_interest = []
    for i in range(0, len(STOCKS)):
        stocks_of_interest.append("T.{}".format(STOCKS[i]))
        stocks_of_interest.append("AM.{}".format(STOCKS[i]))
    listen_data = {"action": "listen", "data": {
        "streams": ["T.AAPL", "AM.AAPL"]}}
    ws.send(json.dumps(listen_data))


def on_message(ws, message):
    message = json.loads(message)
    if(message["stream"] == "authorization" and message["data"]["status"] == "authorized"):
        print("Websocket succesfully authenticated and opened.")
    elif(message["stream"] == "listening"):
        print("Subscribed to {}".format(message["data"]["streams"]))
    elif(message["stream"].startswith("T.")):
        print("Trade of {} at {}".format(
            message["stream"][2:], message["data"]["p"]))
        trade_data[message["data"]["T"]] = (float(message["data"]["p"]), trade_data[message["data"]["T"]][1], trade_data[message["data"]["T"]]
                                            [2], trade_data[message["data"]["T"]][3], trade_data[message["data"]["T"]][4], trade_data[message["data"]["T"]][5])
        # print(trade_data)

    elif(message["stream"].startswith("Q.")):
        print("Quote of {} at {}".format(
            message["stream"][2:], message["data"]["p"]))
    elif(message["stream"].startswith("AM.")):
        print("\n{} at high {} low {} open {} close {}\n".format(
            message["data"]["T"], message["data"]["h"], message["data"]["l"], message["data"]["o"], message["data"]["c"]))
        trade_data[message["data"]["T"]] = (trade_data[message["data"]["T"]][0], float(message["data"]["h"]), float(
            message["data"]["l"]), float(message["data"]["h"]/message["data"]["l"]), float(message["data"]["o"]), float(message["data"]["c"]))
        # print(trade_data)


def on_close():
    print("Connection closed")


def on_error():
    print("Error")


def main():
    for i in range(0, len(STOCKS)):
        # (last trade, last bar high, last bar low, last bar center, last open, last close)
        trade_data[STOCKS[i]] = (0, 0, 0, 0, 0, 0)
    socket = "wss://data.alpaca.markets/stream"
    ws = websocket.WebSocketApp(
        socket, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)
    ws.run_forever()


if __name__ == "__main__":
    main()
