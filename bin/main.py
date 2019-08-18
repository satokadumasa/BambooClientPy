import os
# import sys
import time
from datetime import datetime
import tkinter as Tkinter
import threading
from net.wsclient import WsClient
# from net.cliet import Client
import yaml
# import tkinter as tk

class MainWindow(Tkinter.Frame):
    def __init__(self, master=None):
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

        self.create_widgets()

        self.thread_1 = threading.Thread(target=self.func1)
        self.thread_1.start()
        with open('config/server_info.yaml') as file:
            self.server_info = yaml.load(file, Loader=yaml.SafeLoader)
            print(self.server_info)

#         self.server_info =

    def create_widgets(self):
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

    def run(self):
        self.master.mainloop()

    def stop_app(self):
        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())
        for thread in thread_list:
            thread.join()
            print("All thread is ended.")

    def start_connect(self):
        print("start_connect")
        self.thread_2 = threading.Thread(target=self.connect_to_server)
        self.thread_2.start()

    def connect_to_server(self):
        print("connect_to_server")
        print(self.server_info)
        print("---------------")
        self.cl = WsClient(self.server_info)
        print("---------------")
        self.cl.auth_user()
        print("---------------")
#         cl.connect_websocket()

    def start_chat(self):
        self.cl.start_chat()

    def func1(self):
        now_time = Tkinter.StringVar()
        while True:
            now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            print("now_time:" + now_time)
            self.now_time.set(now_time)
            time.sleep(1)

if __name__ == "__main__":
    os.chdir('../')
    root = Tkinter.Tk()
    mw = MainWindow(master = root)
    mw.run()
