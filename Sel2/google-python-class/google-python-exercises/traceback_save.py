"""
this simple code creates error.log file with traceback error information saved
"""

import traceback
import datetime as dt

def junk():
    return 0/0

def call_junk():
    junk()

try:
    call_junk()
except ZeroDivisionError:
    fp = open('d:\\tmp\\error.log','w')
    fp.write('Error caught @ ' + str(dt.datetime.now()) + '\n\n' )
    traceback.print_exc(file=fp) 
    fp.close()
    
