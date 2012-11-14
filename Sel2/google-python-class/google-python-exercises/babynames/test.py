import os
import sys
import commands

def list(dir):
    filenames = os.listdir(dir)
    for filename in filenames:
        path = os.path.join(dir,filename)
        print path
        print os.path.abspath(path)
        
def run_command(cmd):
    (status,output) = commands. getstatusoutput(cmd)
    if status:
        sys.stderr.write('there was an error:\n' + output)
        sys.exit(1)
    print output




if __name__ =='__main__':
    #cmd = 'D:\workspace\Study\google-python-class\google-python-exercises\babynames\python babynames.py baby1990.html'
    