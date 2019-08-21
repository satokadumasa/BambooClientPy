'''
Created on Aug 21, 2019

@author: k_sato
'''
import PIL
import os
# import sys
import matplotlib
matplotlib.use('tkagg')
import yaml
import glob
import time
import threading
from datetime import datetime
import tkinter as Tkinter
import tkinter.filedialog as tkmsg
from net.wsclient import WsClient
# from net.cliet import Client
from utils.logger import Logger
from webbrowser import BackgroundBrowser

# class TestWindow:
#     def __init__(self,):
#         self.logger = Logger()
#         self.logger.log(['MainWindow', 'init', 'START'])
#         self.master = Tkinter.Tk()
#         screen_width = self. master.winfo_screenwidth()
#         screen_height = self. master.winfo_screenheight()
#         self.master.title(u"Software Title")
#         self.master.geometry('200x200+0+0')
#         self.master.minsize(500, screen_height)
#         self.master.maxsize(screen_width,screen_height)


def add_connect_btn(frame, server_name, server_info, idx):
    print(('MainWindow.add_connect_btn START'))
    print(server_info)
    by = 20 * idx # + 100
    connect_to_server_btn = Tkinter.Button(frame)
    connect_to_server_btn["text"] = server_info['server_name']
    connect_to_server_btn["anchor"] = "w"
    connect_to_server_btn.place(x=5,y=by,width=120,height=20)

root = Tkinter.Tk()
root.geometry("500x200")

# files = glob.glob("config/**/*",  recursive=True)
# print(files)Canvas
file = 'config/server_info.yaml'
with open(file) as file:
    server_infos = yaml.load(file, Loader=yaml.SafeLoader)

# Canvas Widget を生成
canvas = Tkinter.Canvas(root)

# Top Widget上に Scrollbar を生成して配置
bar = Tkinter.Scrollbar(root, orient=Tkinter.VERTICAL)
bar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
bar.config(command=canvas.yview) # ScrollbarでCanvasを制御

# Canvas Widget をTopWidget上に配置
canvas.config(yscrollcommand=bar.set) # Canvasのサイズ変更をScrollbarに通知
canvas.config(scrollregion=(0,0,500,500)) #スクロール範囲
canvas.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=True)

# Frame Widgetを 生成
frame = Tkinter.Frame(canvas)

# Frame Widgetを Canvas Widget上に配置（）
canvas.create_window((20,100), window=frame, anchor=Tkinter.NW, width=500, height=500)


stop_app_btn = Tkinter.Button(frame)
stop_app_btn["text"] = "Exit"
stop_app_btn["anchor"] = "w"
# stop_app_btn["command"] = self.stop_app
stop_app_btn.place(x=20,y=40,width=120,height=20)

connect_to_server_btn = Tkinter.Button(frame)
connect_to_server_btn["text"] = "CONNECT"
connect_to_server_btn["anchor"] = "w"
# connect_to_server_btn["command"] = self.start_connect
connect_to_server_btn.place(x=20,y=60,width=120,height=20)

start_chat_btn = Tkinter.Button(frame)
start_chat_btn["text"] = "CONNECT CHAT"
start_chat_btn["anchor"] = "w"
# start_chat_btn["command"] = self.start_chat
start_chat_btn.place(x=20,y=80,width=120,height=20)

idx = 0
print('-----------')
print(server_infos)
print('-----------')
for server_name, server_info in server_infos['servers'].items():
    print("server_name:" + server_name)
    add_connect_btn(frame, server_name, server_info, idx)
    idx = idx + 1

root.mainloop()
