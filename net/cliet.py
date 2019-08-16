'''
Created on Aug 13, 2019

@author: k_sato
'''
import socket
import requests
import time
from bs4 import BeautifulSoup
import websocket
# import thread

class Client:
    def __init__(self, server_info):
        self.server_info = server_info
        print("Client initialize")
        print(self.server_info)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client initialize CH-01")
#         self.host_name = host_name
#         self.port = port
        self.session = requests.session()
        print("Client initialize CH-02")
        print("Client initialized")
        # サーバを指定
#         self.client.connect((host_name, self.port))

    def auth_user(self):
        print("Client.auth_user ")
        url = 'https://www.hesper.site/users/sign_in'
#         session = requests.session()
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
    def connect_websocket(self):
        print("Client.connect_websocket start")
        print("Client.connect_websocket protcol:" + self.server_info['servers']['default']['protcol'])
        http_origin = self.server_info['servers']['default']['protcol'] + '//' + self.server_info['servers']['default']['server_name']
        print("Client.connect_websocket http_origin:" + http_origin)

        environ = {
            'HTTP_ORIGIN' : http_origin,
            'PATH_INFO' : self.server_info['servers']['default']['websocket_path'],
            'HTTP_HOST' : self.server_info['servers']['default']['server_name']
        }

        self.ws = websocket.WebSocket(environ, self.client, '')
        self.ws.send("sss")

