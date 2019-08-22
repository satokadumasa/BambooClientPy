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

class ListPanel:
    def __init__(self, root):
#         self.playing=playing            # Playing Song Directory
        self.root=Tkinter.Frame(root, bg='skyblue')
        self.root.pack(side='top')
        self.var1=Tkinter.StringVar()       # For Search Songs
        self.directory=Tkinter.StringVar()  # For Directory
        self.directory.set('.')
        self.create_song_list_panel()


    def create_song_list_panel(self):
        # Creating Picture Canvas as Background
#         background=Tkinter.PhotoImage(file="../Icons/background.gif")
        mainframe=Tkinter.Canvas(self.root)
        mainframe.pack(side='top', expand='yes', fill='both')
#         mainframe.image=background
#         mainframe.create_image(0, 0, anchor="nw", image=background)

        frame0=Tkinter.Frame(mainframe)
        frame0.pack(side='top')
        Tkinter.Label(frame0, text='Search : ', bg='skyblue').pack(side='left', expand='yes', fill='x')
        Tkinter.Entry(frame0, textvariable=self.var1).pack(side='left', expand='yes', fill='x')
        frame0.bind_all('<Any-KeyPress>',self.search_song_trigger)

        frame=Tkinter.Frame(mainframe, bg='skyblue')
        frame.pack(side='top')
        self.list_box=Tkinter.Listbox(frame, bg='powderblue', width=500, height=700)
        # スクロールバー
        scrollbar=Tkinter.Scrollbar(frame, bg='skyblue')
        scrollbar.pack(side='right',expand='yes',fill='y')
        scrollbar.config(command=self.list_box.yview)

        self.list_box.config(yscrollcommand=scrollbar.set)

        self.list_box.pack(expand='yes',fill='both',side='right')

        frame1=Tkinter.Frame(mainframe, bg='blue')
        frame1.pack(side='top', expand='yes',fill='x')

        btn1 = Tkinter.Button(self.list_box)
        btn1["text"] = "Btn1"
        btn1.place(x=20, y=10, width=400, height=100)

        btn2 = Tkinter.Button(self.list_box)
        btn2["text"] = "Btn2"
        btn2.place(x=20, y=30, width=400, height=100)


#         add_fileicon=Tkinter.PhotoImage(file="../Icons/add_file.gif")
#         add_directoryicon=Tkinter.PhotoImage(file="../Icons/add_directory.gif")
#         list_file=[
#         (add_fileicon,'self.ask_for_play_song_direct'),
#         (add_directoryicon,'self.ask_for_directory'),
#         ]
#         for i,j in list_file:
#                 storeobj=Tkinter.Button(frame1, image=i, command=eval(j), bg='blue')
#                 storeobj.pack(side='left')
#                 storeobj.image=i
        self.list_box.bind('<Double-Button-1>',self.play_on_click)
        return self.update_list_box_songs()

    def search_song_trigger(self, event=None):
            string=self.var1.get()
            list_dir=os.listdir(self.directory.get())
            self.list_box.delete('0','end')
            for i in list_dir:
                    if string in i:
                            if i[::-1][0]=='~':
                                pass
                            else:
                                self.list_box.insert(0, i)
                    else:
                            pass
            return
    def play_on_click(self, event=None):
            store=self.list_box.selection_get()
            if self.directory.get()=='.':
                    path=os.path.join(os.getcwd(),store)
                    self.playing.set(path)
                    print ('[+] Song Variable Update Path : {}'.format(path))
                    return
            else:
                    path=os.path.join(self.directory.get(),store)
                    self.playing.set(path)
                    print ('[+] Song Variable Update Path : {}'.format(path))
                    return


    def update_list_box_songs(self, dirs='.'):
            files=os.listdir(dirs)
            files.reverse()
            self.list_box.delete('0','end')
            for i in files:
                    if i[::-1][0]=='~':
                            pass
                    else:
                            self.list_box.insert(0, i)
            return


#     def ask_for_play_song_direct(self):
#             path=tkFileDialog.askopenfilename(title='Play Selected Song')
#             if path:
#                     self.playing.set(path)
#                     print ('[+] Song Variable Update Path : {}'.format(path))
#                     return


#     def ask_for_directory(self):
#             path=tkFileDialog.askdirectory(title='Select Directory For Playlist')
#             if path:
#                     self.directory.set(path)
#                     print (path)
#                     return self.update_list_box_songs(dirs=path)

#     def search_song_trigger(self, event=None):
#             string=self.var1.get()
#             list_dir=os.listdir(self.directory.get())
#             self.list_box.delete('0','end')
#             for i in list_dir:
#                     if string in i:
#                             if i[::-1][0]=='~':
#                                 pass
#                             else:
#                                 self.list_box.insert(0, i)
#                     else:
#                             pass
#             return
#     def play_on_click(self, event=None):
#             store=self.list_box.selection_get()
#             if self.directory.get()=='.':
#                     path=os.path.join(os.getcwd(),store)
#                     self.playing.set(path)
#                     print ('[+] Song Variable Update Path : {}'.format(path))
#                     return
#             else:
#                     path=os.path.join(self.directory.get(),store)
#                     self.playing.set(path)
#                     print ('[+] Song Variable Update Path : {}'.format(path))
#                     return

if __name__ == "__main__":
    root = Tkinter.Tk()
#     mw = MainWindow(master = root)
    mw=ListPanel(root)
#     mw = ListPanel()
    root.mainloop()
    mw.run()
