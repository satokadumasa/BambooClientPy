import os
# import sys
import glob
import time
from datetime import datetime
import tkinter as Tkinter
import threading
from net.wsclient import WsClient
# from net.cliet import Client
import yaml
from utils.logger import Logger
from tkinter import Listbox
# import tkinter as tk

class MainWindow(Tkinter.Frame):
    """
    MainWindow初期化
    @param master
    @return: none
    """
    def __init__(self, master=None):
        self.logger = Logger()
        self.logger.log(['MainWindow', 'init', 'START'])
        super().__init__(master)
        self.master = master
        self.master.grid()
        screen_width = self. master.winfo_screenwidth()
        screen_height = self. master.winfo_screenheight()
        self.master.title(u"Software Title")
        self.master.geometry('200x200+0+0')
        self.master.minsize(400, screen_height)
        self.master.maxsize(screen_width,screen_height)

        self.now_time = Tkinter.StringVar()
        self.now_time.set('hello')

        self.read_configs()

        self.create_widgets()

        #時計
        self.tclock_hread = threading.Thread(target=self.clock_start)
        self.tclock_hread.start()

        #契約済みサーバへの接続
        self.connect_to_server_thread = threading.Thread(target=self.connect_to_server)
        self.connect_to_server_thread.start()

    """
    画面生成
    @param none
    @return: none
    """
    def create_widgets(self):
        self.logger.log(['MainWindow', 'create_widgets', 'START'])
        self.stop_app_btn = Tkinter.Button(self.master)
        self.stop_app_btn["text"] = "Exit"
        self.stop_app_btn["anchor"] = "w"
        self.stop_app_btn["command"] = self.stop_app
        self.stop_app_btn.place(x=20,y=40,width=120,height=20)

        self.connect_to_server_btn = Tkinter.Button(self.master)
        self.connect_to_server_btn["text"] = "CONNECT"
        self.connect_to_server_btn["anchor"] = "w"
        self.connect_to_server_btn["command"] = self.start_connect
        self.connect_to_server_btn.place(x=20,y=60,width=120,height=20)

        self.start_chat_btn = Tkinter.Button(self.master)
        self.start_chat_btn["text"] = "CONNECT CHAT"
        self.start_chat_btn["anchor"] = "w"
        self.start_chat_btn["command"] = self.start_chat
        self.start_chat_btn.place(x=20,y=80,width=120,height=20)

        self.label1 = Tkinter.Label(self.master, textvariable=self.now_time, width=20)
        self.label1["anchor"] = "w"
        self.label1.place(x=20,y=20,width=300,height=20)

        print(self.server_info)

        idx = 0
        self.server_list = Listbox(self.master, height=10)
        for server_name, server_info in self.server_info['servers'].items():
            self.server_list.insert(idx, self.creat_connect_btn(server_info))
            idx = idx + 1
        self.server_list.place(x=20,y=100,width=300)


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
    サーバー接続呼び出し
    @param none
    @return: none
    """
    def start_connect(self):
        self.logger.log(['MainWindow', 'start_connect', 'START'])
        self.connect_to_server_thread = threading.Thread(target=self.connect_to_server)
        self.connect_to_server_thread.start()

    """
    サーバー接続
    @param none
    @return: none
    """
    def connect_to_server(self):
        self.logger.log(['MainWindow', 'connect_to_server', 'START'])
        print(self.server_info)
        self.logger.log(['MainWindow', 'connect_to_server', '------------'])
        self.cls = []
        for server_name, server_info in self.server_info['servers'].items():
            self.logger.log(['MainWindow', 'connect_to_server', 'server_name' + server_info['server_name']])
            cl = WsClient(server_info)
            cl.auth_user()
            self.cls.append(cl)
            self.logger.log(['MainWindow', 'connect_to_server', '------------'])
        print(self.cls)
        self.logger.log(['MainWindow', 'connect_to_server', '------------'])

    """
    チャットルーム接続
    @param none
    @return: none
    """
    def start_chat(self):
        self.cl.start_chat()

    """
    時計開始
    @param none
    @return: none
    """
    def clock_start(self):
        now_time = Tkinter.StringVar()
        while True:
            now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            self.now_time.set(now_time)
            time.sleep(1)

    """
    システム終了
    @param none
    @return: none
    """
    def stop_app(self):
        self.logger.log(['MainWindow', 'stop_app', 'START'])
        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())
        for thread in thread_list:
            thread.alive = False
#             thread.join()
            print("All thread is ended.")

    def creat_connect_btn(self, server_info):
        print("server_name:" + server_info['server_name'])
        print(server_info)
        print('-----------------------')
        self.logger.log(['MainWindow', 'connect_to_server', 'server_name' + server_info['server_name']])
        cl = WsClient(server_info)
        connect_to_server_btn = Tkinter.Button(self.master)
        connect_to_server_btn["text"] = server_info['server_name']
        connect_to_server_btn["anchor"] = "w"
        connect_to_server_btn["command"] = cl.start_chat()
#         connect_to_server_btn.place(x=20,y=by,width=120,height=20)
        return connect_to_server_btn


if __name__ == "__main__":
    root = Tkinter.Tk()
    mw = MainWindow(master = root)
    mw.run()
