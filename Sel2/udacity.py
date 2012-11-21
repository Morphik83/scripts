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

def kelivinToFahrenheit(temperature):
    assert(temperature>=0), "Colder than absolute zero!"
    return ((temperature-273)*1.8)+32

def temp_converter(var):
    try:
        return int(var)
    except ValueError, e:
        print "The argument does not contain numbers\n", e
#=================================================================================
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
    print remove_html_markup('xyz')
    print remove_html_markup('"<b>foo</b>"')
    print remove_html_markup("'<b>foo</b>'")


#globals
breakpoints = {81: True}
stepping = False

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
        #my code here
        pass
    elif command.startswith('q'):       #quit
        sys.exit(0)
    else:
        print 'No such command', repr(command)
    
    return False

#commands = ["p", "s", "p tag", "p foo", "q"]
commands = ["s", "s", "q"]

def input_command():
    #command = raw_input("(my-spider)")
    global commands
    command = commands.pop(0)
    return command

def traceit(frame, event, trace_arg):
    global stepping
    
    if event  == 'line':
        if stepping or breakpoints.has_key(frame.f_lineno):
            resume = False
            while not resume:
                print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals
                command = input_command()
                resume = debug(command, frame.f_locals)
    return traceit

#Using the tracer
sys.settrace(traceit)
main()
sys.settrace(None)



