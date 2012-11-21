import sys
import linecache
filename = 'trace_python_code.py'

def traceit(frame, event, arg):
    if event == "line":
        lineno = frame.f_lineno
        line = linecache.getline(filename, lineno)
        print "line %d: %s" % (lineno, line.rstrip())
    
    return traceit

def main():
    print "In main"
    for i in range(5):
        print i, i*3
    print "Done."

sys.settrace(traceit)
main()