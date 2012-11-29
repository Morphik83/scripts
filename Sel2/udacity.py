from mhlib import isnumeric
def remove_html_markup_FIXED(s):
    tag = False
    quote = False
    out = ""
    for c in s:
        if quote and not tag:
            raise ValueError
        
        if c == "<" and not quote:    #Start of markup
            tag = True
        elif c == ">" and not quote:
            tag = False
       
        #=======================================================================
        # elif c == '"' or c == "'" and tag:
        #    quote = not quote
        # OR has lower precedence than AND, so code would be interpreted as:
        # elif c == '"' or (c == "'" and tag)
        # So, if c=='"' -> TRUE. OR returns first TRUE, so next condition(AND) is not being checked
        # and the 'quote=not quote' is executed (" is stripped in that way)
        # On the other hand, it c=="'", then second condition is executed, but 'tag' is FALSE, so 
        # 'quote=not quote' is NOT executed, and that is why "'" is stripped from string.
        # FIRST SOLUTION: elif (c == '"' or c == "'") and tag
        #
        # SECOND SOLUTION:
        # possible states of this program: ^quoteAND^tag ->occurs > -> ^quoteANDtag -> quoteANDtag -> ^quoteANDtag -> ^quoteAND^tag
        # we do not want to have: quoteAND^tag (so qu otes outside of the tags) -> this code should never be reached
        # IF (quotesAND^tag) raise error
        #          ==
        # IF NOT !(quotesAND^tag) raise error
        #          ==
        # IF NOT (tagOR^quotes) raise error
        #          ==
        # assert tag or not quotes -> this statement put at the very beginning to avoid erroneous behavior 
        # or put: if quote and not tag:
        #            raise ValueError
        # this is the same as assert!
        #=======================================================================
        
        elif c == '"' or c == "'" and tag:  #quote can be true only when tag is true! 
            quote = not quote
        elif not tag:
            out = out + c
    return out

#===============================================================================
# assert condition is the same as:
# if __debug__:
#    if not condition: raise AssertionError
#===============================================================================
#===============================================================================
# 
# 
# 
# if __name__ == '__main__':
#   s="'foo'"
#   print remove_html_markup(s)
#===============================================================================
    


import sys
try:
    import pyreadline as readline
except ImportError:
    import readline

#Our buggy program
def remove_html_markup(s):
    tag    = False
    quote  = False
    out    = ""
    
    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out 

#main program that runs the buggy code
def main():
    #print "main():", remove_html_markup('xyz')
    print "main():", remove_html_markup('"<b>foo</b>"')
    #print remove_html_markup("'<b>foo</b>'")


#globals
breakpoints = {71: True}
stepping = False
watchpoints = {'c':True}

def debug(command, my_locals):
    global breakpoints
    global stepping
    
    if command.find(' ') > 0:
        arg = command.split(' ')[1]
    else:
        arg = None
    
    if command.startswith('s'):         #step
        stepping = True
        return True
    elif command.startswith('c'):        #continute
        stepping = False
        return True
    elif command.startswith('p'):       #print
        if arg:                                #arg defined in line 112
            if my_locals.has_key(arg):              #check if arg in my_locals
                print arg,"=", repr(my_locals[arg])
            else:
                print 'No such variable:',arg
        else:
            print 'my_locals:',my_locals        #if print cmd has no args, 
                                                #print out whole dict 
           #cannot return True! If True, then (p) would also switch to the next line
           #we do not want it! (s) is for stepping, (p) if for printing 
           #all the local variables in the current line, and only this!  
           #Not stepping (next line)!
    elif command.startswith('b'):
       if arg and int(arg) in range(71,85):          #line no.71 - script starts, 95-ends
           breakpoints[int(arg)]=True
           print "breakpoints:",breakpoints
       else:
           print 'You must supply a line number'
    elif command.startswith('w'):
        if arg:
            watchpoints[arg]=True
        else:
            print 'You must supply a variable name' 
            
    elif command.startswith('q'):       #quit
        sys.exit(0)
    else:
        print 'No such command', repr(command)
    
    return False

#commands = ["b 85", "p", "s", "p", "s", "p", "c","p","c", "q"]
#commands = ["w out", "c"]
def input_command():
    command = raw_input("(my-spider):")
    #global commands
    #command = commands.pop(0)
    return command

def traceit(frame, event, trace_arg):
    global stepping

    if event  == 'line':
        print "event: ",event," ,line_No: ",frame.f_lineno
        
        #watchpoints on each item
        if watchpoints.items() > 0 :
            for item in watchpoints:
                print "ITEM:",item
                print "frame.f_locals:",frame.f_locals
                if item in frame.f_locals:
                    print "Watch:",item,"Value:",frame.f_locals[item]
                    
        if stepping or breakpoints.has_key(frame.f_lineno):
            print "stepping: ",stepping ,', bPoint: ',breakpoints.has_key(frame.f_lineno)
            resume = False
            while not resume:
                #print "inWhile: ",event, frame.f_lineno, frame.f_code.co_name, frame.f_locals
                command = input_command()
                print "command: ", command
                resume = debug(command, frame.f_locals)
                print 'resume', resume,"\n", 20*"-"
    print ">>>>next event<<<<"
    return traceit

#Using the tracer
if __name__ == '__main__':
    sys.settrace(traceit)
    main()
    sys.settrace(None)

#===============================================================================
# print breakpoints
# debug("b 92",{'quote': False, 's': 'xyz', 'tag': False, 'c': 'b', 'out': ''})
# print breakpoints == {81: True, 92:True}
#===============================================================================


