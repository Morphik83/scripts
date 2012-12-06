#!/usr/bin/python
import sys

    #print is just a thin wrapper that formats the inputs 
    #(space between args and newline at the end) and calls the write function of 
    #a given object. By default this object is sys.stdout but you can pass a file for example:
    #print >> open('file.txt', 'w'), 'Hello', 'World', 2+3


 
# a simple class with a write method
class WritableObject:
    def __init__(self):
        self.content = []
    def write(self, string):
        self.content.append(string)
        
        
# another simple class to write parallelly to std.out and log file
class Logger(object):
    def __init__(self, filename="Default_Redirect.log"):
        self.log = open(filename, 'a+')
        self.terminal = sys.stdout
        self.content = []
    def write(self, text):
        self.log.write(text)
        self.terminal.write(text)
        self.content.append(text)
    def close(self):
        self.log.close()
        self.terminal.close()
        
        
        
        
        
        
#for testing purposes        
if __name__ == '__main__':
    # example with redirection of sys.stdout
    foo = WritableObject()                   # a writable object
    sys.stdout = foo
    sys.stdout.write('xxxxxxx')                         # redirection
    print "one, two, three, four"            # some writing
    sys.stdout = sys.__stdout__              # remember to reset sys.stdout!
    print "foo's content:", foo.content                # show the result of the writing
     
    # example with redirection of the print statement
    bar = WritableObject()                   # another writable object
    print >>bar, "one, two, three, four"     # some (redirected) writing
    print >>bar, "little hat made of paper"
    print "bar's content:", bar.content
    
    # example of Logger use
    sys.stdout = Logger('D:\\tmp\\MyTestLogFile.log')
    print 'Hello!'     #this should be logged as well into log file 
    
