'''
Created on Aug 17, 2019

@author: k_sato
'''
import socket
import websocket
from bs4 import BeautifulSoup
from threading import Thread
import time
import requests
# import sys

class WsClient:
    def __init__(self, server_info):
#             host = "ws://www.hesper.site:3000/"
        print("WsClient.init")
#         print(server_info)
        self.server_info = server_info
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session = requests.session()
#         print("WsClient.init CH-01")
#         print("WsClient.init server_name" + self.server_info['servers']['default']['server_name'] + "/cable")
#         print("WsClient.init ws_port" + str(self.server_info['servers']['default']['port']))
        self.host = "ws://" + self.server_info['servers']['default']['server_name'] + ":" + str(self.server_info['servers']['default']['ws_port']) + "/cable"
#         print("WsClient.init host:" + self.host)
        self.ws = websocket.WebSocketApp(self.host,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
#         print("WsClient.init on_open:")
        self.ws.on_open = self.on_open
#         print("WsClient.init run_forever:")
        self.ws.run_forever()

    def on_message(self, message):
        print("on_message")
        print(self.ws)
        print(message)


    def on_error(self, error):
        print("on_error")
        print(self.ws)
        print(error)


    def on_close(self):
        print("on_close")
        print(self.ws)
        print("### closed ###")


    def on_open(self):
        print("###on_open###")
        def run():
            print("###run###")
            print("run")
            print(self.ws)
            for i in range(3):
                # send the message, then wait
                # so thread doesn't exit and socket
                # isn't closed
                print("ws send...")
                self.ws.send("Hello %d" % i)
                print("time sleep...")
                time.sleep(1)

            time.sleep(1)
            self.ws.close()
            print("Thread terminating...")

        print("Thread call run")
        Thread(target=run).start()

    # 認証処理
    def auth_user(self):
        print("Client.auth_user ")
        url = 'https://www.hesper.site/users/sign_in'
        response = self.session.get(url)

        # BeautifulSoupオブジェクト作成(token取得の為)
        bs = BeautifulSoup(response.text, 'html.parser')

        login_data = {
           'UTF-8': '✓',
           'session[email]': 'sato.kadumasa@gmail.com',
           'session[password]': 'glxre297',
        }

        # tokenの取得
        authenticity_token = bs.find(attrs={'name':'authenticity_token'}).get('value')

        # 取得したtokenをpostするパラメータに追加
        login_data['authenticity_token'] = authenticity_token

        login_data = self.session.post(url, data=login_data)
        time.sleep(2)
        print(login_data.text)

