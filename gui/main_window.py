'''
Created on Aug 25, 2019

@author: k_sato
'''
# import PIL
import os
import yaml
import json
import glob
import time
from threading import (Event, Thread)
from datetime import datetime
import tkinter as Tkinter
from utils.logger import Logger
from net.wsclient import WsClient
from gui.client_window import ClientWindow

class MainWindow:
    """
    MainWindow初期化
    @param master
    @return: none
    """
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
    def __init__(self):
        self.logger = Logger()
        self.logger.log(['System Start\n=====================================\nBambooClientPy\nSince 2019\nAuthor: Kadumasa Sato\n====================================='])
        self.master = Tkinter.Tk()
        # screen_width = self. master.winfo_screenwidth()
        screen_height = self. master.winfo_screenheight()
        self.master.title(u"Bamboo Client")
        self.master.geometry('300x700')
        self.master.minsize(320, 700)
        self.master.maxsize(320,screen_height)

        self.now_time = Tkinter.StringVar()
        self.now_time.set('hello')

        # 設定ファイル読み込み
        self.read_configs()
        #契約済みサーバへの接続
        self.connect_to_server()
        # 画面生成
        self.create_widgets()

        #時計
        self.clock_event = Event()
        self.tclock_hread = Thread(target=self.clock_start)
        self.tclock_hread.start()

    """
    画面生成
    @param none
    @return: none
    """
    def create_widgets(self):
        self.logger.log(['MainWindow', 'create_widgets', 'START'])
        # Server List 用Frameを生成
        self.master.title("Toy")
        self.master.geometry("+20+20")

        self.label1 = Tkinter.Label(self.master, textvariable=self.now_time, width=20)
        self.label1["anchor"] = "w"
        self.label1.place(x=0,y=20,width=300,height=20)

        self.stop_app_btn = Tkinter.Button(self.master)
        self.stop_app_btn["text"] = "Exit"
        self.stop_app_btn["anchor"] = "w"
        self.stop_app_btn["command"] = self.stop_app
        self.stop_app_btn.place(x=0,y=40,width=120,height=20)

        self.connect_to_server_btn = Tkinter.Button(self.master)
        self.connect_to_server_btn["text"] = "RECONNECT"
        self.connect_to_server_btn["anchor"] = "w"
        self.connect_to_server_btn["command"] = self.start_connect
        self.connect_to_server_btn.place(x=0,y=60,width=120,height=20)

        self.add_server_list()
        self.add_update_contents_list()

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
    主処理
    @param none
    @return: none
    """
    def run(self):
        self.logger.log(['MainWindow', 'run', 'START'])
        self.master.mainloop()

    """
    時計開始
    @param none
    @return: none
    """
    def clock_start(self):
        now_time = Tkinter.StringVar()
        while not self.clock_event.wait(1):
            now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            self.now_time.set(now_time)

        time.sleep(1)

    """
    システム終了
    @param none
    @return: none
    """
    def stop_app(self):
        print("MainWindow.stop_app")
        self.clock_event.set()
        self.master.destroy()

    """
    サーバリスト
    @param none
    @return: none
    """
    def add_server_list(self):
        # Server List 表示 を生成
        print( len(self.server_info['servers']))
        server_list = Tkinter.Frame(self.master)
        server_list.place(x=0,y=80,width=320,height=100)

        canvas = Tkinter.Canvas(server_list)

        # Server List 表示 Frame上に Scrollbar を生成して配置
        bar = Tkinter.Scrollbar(server_list, orient=Tkinter.VERTICAL)
        bar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        bar.config(command=canvas.yview) # ScrollbarでCanvasを制御

        # Canvas Widget をServer List 表示 Frame上に配置
        canvas.config(yscrollcommand=bar.set) # Canvasのサイズ変更をScrollbarに通知
        canvas.config(scrollregion=(0,0,300,20 * len(self.server_info['servers']))) #スクロール範囲
        canvas.place(x=0,y=0,width=300,height=100)

        # Frame Widgetを 生成
        self.server_list_frame = Tkinter.Frame(canvas)
        # 表示
        canvas.create_window((0,0), window=self.server_list_frame, anchor=Tkinter.NW, width=400, height=20 * len(self.server_info['servers']))

        idx = 0
        for server_name, server_info in self.server_info['servers'].items():
            self.add_connect_btn(server_name, server_info, idx)
            idx = idx + 1

    """
    ラウンジ接続
    @param none
    @return: none
    """
    def add_connect_btn(self, server_name, server_info, idx):
        print('MainWindow.add_connect_btn START')
        print(server_info)
        self.logger.log(['MainWindow', 'connect_to_server', 'server_name' + server_name])
        by = 20 * idx
        connect_to_server_btn = Tkinter.Button(self.server_list_frame)
        connect_to_server_btn["text"] = server_info['site_name']
        connect_to_server_btn["anchor"] = "w"
        connect_to_server_btn.config(command= lambda: self.open_client_window(server_name))
        connect_to_server_btn.place(x=0,y=by,width=300,height=20)

    """
    コンテンツ更新情報
    @param none
    @return: none
    """
    def add_update_contents_list(self):
        # Server List 表示 を生成
        print( len(self.server_info['servers']))
        list_frame = Tkinter.Frame(self.master)
        list_frame.place(x=0,y=200,width=400,height=200)

        canvas = Tkinter.Canvas(list_frame)

        # Server List 表示 Frame上に Scrollbar を生成して配置
        bar = Tkinter.Scrollbar(list_frame, orient=Tkinter.VERTICAL)
        bar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        bar.config(command=canvas.yview) # ScrollbarでCanvasを制御

        # Canvas Widget をServer List 表示 Frame上に配置
        canvas.config(yscrollcommand=bar.set) # Canvasのサイズ変更をScrollbarに通知
        canvas.config(scrollregion=(0,0,300,20 * len(self.server_info['servers'])), bg="black") #スクロール範囲
        canvas.place(x=0,y=0,width=300,height=100)

        # Frame Widgetを 生成
        self.update_contents_list_frame = Tkinter.Frame(canvas)
        # 表示
        canvas.create_window((0,0), window=self.update_contents_list_frame, anchor=Tkinter.NW, width=400, height=20 * len(self.server_info['servers']))

    """
    サーバー接続呼び出し
    @param none
    @return: none
    """
    def start_connect(self):
        self.logger.log(['MainWindow', 'start_connect', 'START'])
        self.connect_to_server_event = Event()
        self.connect_to_server_thread = Thread(target=self.connect_to_server)
        self.connect_to_server_thread.start()

    """
    サーバー接続
    @param none
    @return: none
    """
    def connect_to_server(self):
        self.logger.log(['MainWindow', 'connect_to_server', 'START'])
        self.cls = {}
        for server_name, server_info in self.server_info['servers'].items():
            self.logger.log(['MainWindow', 'connect_to_server', 'server_name' + server_info['server_name']])
            cl = WsClient(server_info)
            cl.auth_user()
            self.cls[server_name] = cl

        self.logger.log(['MainWindow', 'connect_to_server', 'END'])

    """
    @param server_name String
    @return: none
    """
    def open_client_window(self, server_name):
        self.logger.log(['MainWindow', 'open_client_window', 'server_name' + server_name])
        clw = ClientWindow(self.cls[server_name])
        clw.run()
