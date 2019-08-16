'''
Created on Aug 17, 2019

@author: k_sato
'''

import websocket
# from threading import Thread
# import time
import os
# import sys
from net.wsclient import WsClient

# class WsClient:
#     def __init__(self, host):
#         print("Client.init")
#         self.host = host
#     def on_message(self, ws, message):
#         print(message)
#
#
#     def on_error(self, ws, error):
#         print(error)
#
#
#     def on_close(self, ws):
#         print("### closed ###")
#
#
#     def on_open(self, ws):
#         def run(*args):
#             for i in range(3):
#                 # send the message, then wait
#                 # so thread doesn't exit and socket
#                 # isn't closed
#                 ws.send("Hello %d" % i)
#                 time.sleep(1)
#
#             time.sleep(1)
#             ws.close()
#             print("Thread terminating...")
#
#         Thread(target=run).start()


if __name__ == "__main__":
    os.chdir('../')

    websocket.enableTrace(True)
#     if len(sys.argv) < 2:
    host = "ws://www.hesper.site:3000/"
#     else:
#         host = sys.argv[1]

    cl = WsClient(host)
#     ws = websocket.WebSocketApp(host,
#                                 on_message=cl.on_message,
#                                 on_error=cl.on_error,
#                                 on_close=cl.on_close)
#     ws.on_open = cl.on_open
#     ws.run_forever()
