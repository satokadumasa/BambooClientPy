'''
Created on Aug 17, 2019

@author: k_sato
'''
from datetime import datetime

class Logger:
    """
    Initialize Logger class
    @param none
    @return:  none
    """
    def __init__(self):
        today = datetime.now().strftime("%Y%m%d")
        self.log_file_name = 'tmp/log/debug_' + today + '.log'

    """
    Log out put
    @param messages list
    @return:  none
    """
    def log(self, messages):
        fp = open(self.log_file_name,'a')
        now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        message = now_time + ': ' + ' '.join(messages) + "\n"
        fp.write(message)
        fp.close()
