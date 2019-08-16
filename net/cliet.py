'''
Created on Aug 13, 2019

@author: k_sato
'''
import socket

class Client:
    def __init__(self, host_name='localhost', port=443):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_name = host_name
        self.port = port
        # サーバを指定
        self.sv.connect((host_name, self.port))

    def sss(self):
        # サーバにメッセージを送る
        self.sv.sendall(b'hello')
        # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
        data = self.sv.recv(1024)
        #
        print(repr(data))
