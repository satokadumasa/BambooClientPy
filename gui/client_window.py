'''
Created on Aug 25, 2019

@author: k_sato
'''
# import PIL
import os
import json
import yaml
import glob
import time
# import threading
from threading import (Event, Thread)
from datetime import datetime
import tkinter as Tkinter
from utils.logger import Logger
from net.wsclient import WsClient

class ClientWindow:
    """
    MainWindow初期化
    @param master
    @return: none
    """
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
    def __init__(self, ws_client):
        self.logger = Logger()
        self.logger.log(['ClientWindow', 'nit', 'START'])
        self.ws_client = ws_client

        self.master = Tkinter.Tk()
        screen_width = self. master.winfo_screenwidth()
        screen_height = self. master.winfo_screenheight()
        self.master.title(u"Software Title")
        self.master.geometry('700x700+360+0')
        self.master.minsize(700, 700)
        self.master.maxsize(screen_width,screen_height)

        # 画面生成
        self.create_widgets()
        # チャットルーム一覧取得
        self.get_lounges()
        # チャットルーム一覧生成・表示
        self.add_lounges_list()

    def get_lounges(self):
        lounges = self.ws_client.get_lounges()
        self.logger.log(['ClientWindow', 'get_lounges', 'lounges.text'])
        self.lounges_list = json.loads( lounges.text)
        self.user = self.ws_client.login_data.text


    """
    ラウンジ一覧
    @param none
    @return: none
    """
    def add_lounges_list(self):
        # Server List 表示 を生成
        list_frame = Tkinter.Frame(self.master)
        list_frame.place(x=0,y=20,width=320,height=200)

        canvas = Tkinter.Canvas(list_frame)

        # Server List 表示 Frame上に Scrollbar を生成して配置
        bar = Tkinter.Scrollbar(list_frame, orient=Tkinter.VERTICAL)
        bar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        bar.config(command=canvas.yview) # ScrollbarでCanvasを制御

        # Canvas Widget をServer List 表示 Frame上に配置
        canvas.config(yscrollcommand=bar.set) # Canvasのサイズ変更をScrollbarに通知
        canvas.config(scrollregion=(0,0,300,300), bg="black") #スクロール範囲
        canvas.place(x=0,y=0,width=300,height=300)

        # Frame Widgetを 生成
        self.lounges_list_frame = Tkinter.Frame(canvas)
        # 表示
        canvas.create_window((0,0), window=self.lounges_list_frame, anchor=Tkinter.NW, width=400, height=200)

        idx = 0

        if hasattr(self, 'lounges_list') and len(self.lounges_list) > 0:
            for chat_room_info in self.lounges_list:
                print(chat_room_info)
                self.add_connect_chat_room_btn(chat_room_info, idx)
                idx = idx + 1

    def add_connect_chat_room_btn(self, chat_room_info, idx):
        self.logger.log(['MainWindow', 'connect_to_server', 'chat_room' + chat_room_info['title']])
        by = 20 * idx
        connect_to_server_btn = Tkinter.Button(self.lounges_list_frame)
        connect_to_server_btn["text"] = chat_room_info['title']
        connect_to_server_btn["anchor"] = "w"
        connect_to_server_btn.config(command= lambda: self.start_chat(chat_room_info))
        connect_to_server_btn.place(x=0,y=by,width=300,height=20)

    """
    チャットルーム接続
    @param none
    @return: none
    """
    def start_chat(self, chat_room_info):
        print('MainWindow.start_chat title:' + chat_room_info['title'])
        self.logger.log(['MainWindow', 'connect_to_server', 'start_chat' + chat_room_info['title']])
        self.ws_client.remark(self, 'attend', chat_room_info['lounge_id'])

    """
    画面生成
    @param none
    @return: none
    """
    def create_widgets(self):
        self.logger.log(['MainWindow', 'create_widgets', 'START'])

    """
    主処理
    @param none
    @return: none
    """
    def run(self):
        self.logger.log(['MainWindow', 'run', 'START'])
        self.master.mainloop()

    """
    設定ファイル読み込み
    @param none
    @return: none
    """
    def read_configs(self):
        self.logger.log(['MainWindow', 'read_configs', 'START'])
        files = glob.glob("config/**/*",  recursive=True)
        print(files)
        for file in files:
            self.logger.log(['MainWindow', 'read_configs', 'file:' + file])
            name, ext = os.path.splitext(file)
            self.logger.log(['MainWindow', 'read_configs', 'name:' + name, 'ext:' + ext])
            if ext != '.yaml':
                continue
            config_name = name.split('/')[-1]
            self.logger.log(['MainWindow', 'read_configs', 'config_name:' + config_name])
            with open(file) as file:
                conf = yaml.load(file, Loader=yaml.SafeLoader)
                exec('self.{} = {}'.format(config_name, conf))
        print(self.server_info)

    """
    システム終了
    @param none
    @return: none
    """
    def stop_app(self):
        self.logger.log(['ClientWindow', 'stop_app', 'START'])
#         thread_list = threading.enumerate()
#         thread_list.remove(threading.main_thread())
#         for thread in thread_list:
#             thread.alive = False
# #             thread.join()
#             print("All thread is ended.")
