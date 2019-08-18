'''
Created on Aug 17, 2019

@author: k_sato
'''
class Logger:
    def __init__(self):
        f = open('tmp/log/debig.log','w')
        f.write('hoge\n')
        f.close()
        