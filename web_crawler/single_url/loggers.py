from config_file import *
import sys

# another simple class to write parallelly to std.out and log file
class Logger(object):
    def __init__(self, filename):
        self.log = open(filename, 'a+') 
        self.terminal = sys.stdout          #all the data form sys.stdout printed to terminal 
        
    def write(self, text):
        self.log.write(text)
        self.terminal.write(text)
        
    def close(self):
        self.log.close()
        self.terminal.close()