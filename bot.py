import websocket, talib, json, numpy
from binance.client import Client
from binance.enums import *
import config


SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.05
closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET, tld='uk')

def on_open(ws):
    print('Opened connection')
    
def on_close(ws):
    print('Closed connection')

def on_message(ws, message):
    global closes
    print('received message')
    json_message = json.loads(message)
    print(json_message)
    
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)
        
        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("All rsis calculated so far")
            print(rsi) 
            last_rsi = rsi[-1]
            print("The current RSI is: {}".format(last_rsi))   
            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("sell!")
                    #put binance sell logic here
                else:
                    print("We don't own any. Nothing to do.")
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("it is oversold but you already own it")
                else:
                    print("Buy!")
                    #put binance order logic here         
        
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()