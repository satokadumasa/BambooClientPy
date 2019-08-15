#!/Users/k_sato/.pyenv/shims/python
# -*- coding: utf8 -*-
#import matplotlib
#matplotlib.use('Agg')

import sys
import time
from datetime import datetime
import tkinter as Tkinter
import threading
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

    def create_widgets(self):
#         self.stop_app_btn = Tkinter.Button( self.master,  text=u"QUIT",  command=self.stop_app)
#         self.stop_app_btn.pack(side="bottom")
        self.stop_app_btn = Tkinter.Button(self.master)
        self.stop_app_btn["text"] = "Exit"
        self.stop_app_btn["command"] = self.stop_app
        self.stop_app_btn.pack(side="top")

        self.label1 = Tkinter.Label(self.master, textvariable=self.now_time, width=20)
        self.label1.pack()

    def run(self):
       self.master.mainloop()

    def stop_app(self):
        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())
        for thread in thread_list:
            thread.join()
            print("All thread is ended.")

    def func1(self):
        now_time = Tkinter.StringVar()
        while True:
            now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            print("now_time:" + now_time)
            self.now_time.set(now_time)
            time.sleep(1)

if __name__ == "__main__":
    root = Tkinter.Tk()
    mw = MainWindow(master = root)
    mw.run()
