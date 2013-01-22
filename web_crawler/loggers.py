from config_file import *
import sys

# another simple class to write parallelly to std.out and log file
class Logger(object):
    def __init__(self, filename=crawler_log):
        self.log = open(filename, 'a+')
        self.terminal = sys.stdout
        
    def write(self, text):
        self.log.write(text)
        self.terminal.write(text)
        
    def close(self):
        self.log.close()
        self.terminal.close()