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
    # 初期化
    def __init__(self, server_info):
        print("WsClient.init")
        # 接続先情報受け取り
        self.server_info = server_info
        print("-------------------")
        print(self.server_info)
        print("-------------------")
        # 通常ソケットの生成
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # セッション生成
        self.session = requests.session()

    def start_chat(self):
        # Websocket用意
        ws_url = "ws://" + self.server_info['servers']['default']['server_name'] + ":" + str(self.server_info['servers']['default']['ws_port']) +  self.server_info['servers']['default']['websocket_path']
        self.ws = websocket.WebSocketApp(ws_url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        # 通信ポーリング
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    # メッセージ受信
    def on_message(self, message):
        print("on_message")
        print(self.ws)
        print(message)

    # エラーハンドリング
    def on_error(self, error):
        print("on_error")
        print(self.ws)
        print(error)

    # Websocketのクローズ
    def on_close(self):
        print("on_close")
        print(self.ws)
        print("### closed ###")

    # 通信ポーリング
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
        url = self.server_info['servers']['default']['protcol'] + '://' + self.server_info['servers']['default']['server_name'] + self.server_info['servers']['default']['sign_in_url']
        print('sign_in_url > ' + url)
        response = self.session.get(url)

        # BeautifulSoupオブジェクト作成(token取得の為)
        bs = BeautifulSoup(response.text, 'html.parser')

        login_data = {
           'UTF-8': '✓',
           'email': self.server_info['servers']['default']['user_name'],
           'password': self.server_info['servers']['default']['password'],
        }

        # tokenの取得
        authenticity_token = bs.find(attrs={'name':'authenticity_token'}).get('value')

        # 取得したtokenをpostするパラメータに追加
        login_data['authenticity_token'] = authenticity_token

        # ログインAPI実行
        url = self.server_info['servers']['default']['protcol'] + '://' + self.server_info['servers']['default']['server_name'] + self.server_info['servers']['default']['api_sign_in_url']
        print('api_sign_in_url > '   + url)

        # 実行結果
        login_data = self.session.post(url, data=login_data)
        time.sleep(2)
        print(login_data.text)

