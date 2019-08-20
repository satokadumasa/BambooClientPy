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
from utils.logger import Logger
# import sys

class WsClient:
    # 初期化
    def __init__(self, server_info):
        self.logger = Logger()
        self.logger.log(['WsClient', 'init', 'START'])
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
        print("WsClient.start_chat")
        self.logger.log(['WsClient', 'start_chat', 'START'])
        # Websocket用意
        ws_url = "ws://" + self.server_info['server_name'] + ":" + str(self.server_info['ws_port']) +  self.server_info['websocket_path']
        self.ws = websocket.WebSocketApp(ws_url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        # 通信ポーリング
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    # メッセージ受信
    def on_message(self, message):
        self.logger.log(['WsClient', 'on_message', 'START'])
        print(self.ws)
        print(message)

    """
    エラーハンドリング
    @param error
    @return:  none
    """
    def on_error(self, error):
        self.logger.log(['WsClient', 'on_error', 'START'])
        print("WsClient.on_error")
        print(self.ws)
        print(error)

    """
    Websocketのクローズ
    @param none
    @return:  none
    """
    def on_close(self):
        print("WsClient.on_close")
        print(self.ws)
        print("### closed ###")

    """
    通信ポーリング
    @param none
    @return:  none
    """
    def on_open(self):
        self.logger.log(['WsClient', 'on_open', 'START'])
        print("Thread call run")
        Thread(target=self.run).start()

    """
    クライアント
    @param none
    @return:  none
    """
    def run(self):
        self.logger.log(['WsClient', 'run', 'START'])
        print("WsClient.run")
        print(self.ws)
        for i in range(30):
            # send the message, then wait
            # so thread doesn't exit and socket
            # isn't closed
            print("ws send...")
            self.ws.send("Hello %d" % i)
            print("Hello %d" % i)
            print("time sleep...")
            time.sleep(1)

        time.sleep(1)
        self.ws.close()
        print("Thread terminating...")

    """
    認証処理
    @param none
    @return:  none
    """
    def auth_user(self):
        print("Client.auth_user ")
        url = self.server_info['protcol'] + '://' + self.server_info['server_name'] + self.server_info['sign_in_url']
        print('sign_in_url > ' + url)
        try:
            response = self.session.get(url)
            print("status_code: " +str(response.status_code))
            # BeautifulSoupオブジェクト作成(token取得の為)
            bs = BeautifulSoup(response.text, 'html.parser')
            login_data = {
               'UTF-8': '✓',
               'email': self.server_info['user_name'],
               'password': self.server_info['password'],
            }

            # tokenの取得
            authenticity_token = bs.find(attrs={'name':'authenticity_token'}).get('value')

            # 取得したtokenをpostするパラメータに追加
            login_data['authenticity_token'] = authenticity_token

            # ログインAPI実行
            url = self.server_info['protcol'] + '://' + self.server_info['server_name'] + self.server_info['api_sign_in_url']
            print('api_sign_in_url > '   + url)

            # 実行結果
            login_data = self.session.post(url, data=login_data)
            time.sleep(2)
            self.status = 'able'
            print(login_data.text)
        except requests.exceptions.RequestException:
            self.status = 'able'
