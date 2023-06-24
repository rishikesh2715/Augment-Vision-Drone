# current implementation of the Flutterometer /FLIPASED communication
# reads the data from the websocket provided by thibaults telemetry server

import websocket
import socket
import json


try:
    import thread
except ImportError:
    import _thread as thread
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 50013
MESSAGE = "23,567,32,4356,456,132,4353467"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
try:
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
except:
    print('Initial message failed!')


def on_message(ws, message):
    #print(message)
    # parse the incoming message
    jsonParse = json.loads(message)
    #print(jsonParse)
    ID = jsonParse['FLIPASED']['id']
    freq = jsonParse['FLIPASED']['freq']
    damp = jsonParse['FLIPASED']['damp']
    timest = jsonParse['FLIPASED']['timest']

    
    # Build a message, to add more data add new curly bracket and variable name
    MESSAGE = "{},{},{},{}".format(ID, freq, damp, timest)
    # Show the timestep
    print(MESSAGE)
    #print(type(MESSAGE))
    print('\n')

    # Pumping out the values
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("open")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.0.173:443", #IP and port of thibaults servers websocket
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
