
""""
ToDo:
-unify all the returned headers (the same name!)
-add logging 
-add graph to make analyzing results easier 
-parallelly write to std.out and log
"""

#>MASTER changes + BRANCH changes

import pprint
import re
import sys
import loggers
import time
import urllib2
import pprint

foo = loggers.Logger()   #redirect all the outputs to the foo 
sys.stdout = foo

#srh = SmartRedirectHandler(log)        #redirect handler with extra headers
#handler = urllib2.HTTPHandler()
#handler.set_http_debuglevel(1)
opener = urllib2.build_opener()
opener.handle_open['http'][0].set_http_debuglevel(1)
request = urllib2.Request('http://www.volvo.com')
try:
     opener.open(request)
     #pprint.pprint(f.__dict__)
except Exception, e:
    print "There was a problem with opening URL. Error: ",e
finally:
    sys.stdout = sys.__stdout__                 #revert sys.stdout to normal
    
    
"""OUTPUT PARSER - input: Logger.content list
opener.open(request) writes to Logger.content since sys.stdout is redirected!

"""
log='D:\\tmp\\xxxxxx.log'       #detailed final log file
logger = loggers.Logger(log)
sys.stdout = logger

"""
in original response there are following tags:
    send: 'GET / HTTP/1.1\r\nAccept-Encoding: identity\r\nHost: www.volvopenta.com\r\nConnection: close\r\nUser-Agent: Python-urllib/2.7\r\n\r\n'
    reply: 'HTTP/1.1 301 Moved Permanently\r\n'
    (...)
    header: Location: http://www.volvopenta.com/volvopenta/splash/en-gb
    (...)
Below patterns are used to make sure that proper line was selected (GET/HEAD/Locastion) 
"""
pattern_send = re.compile(r'^\'GET.*$')          #prepare regexp patterns 
pattern_reply = re.compile(r'^\'HTTP.*$')
pattern_location = re.compile(r'\bLocation\b.*$')

"""
Use below regexps, 
when proper line is already selected, to extract relevant info, like:
-HOST, URL used to create GET request,
-response CODE (Status = 302/301/200/...)
-target URL 
"""
pattern_send_1 = re.compile(r'^\'GET\s(.*)\sHTTP.*Host:\s(.*)Connection')  #URL used to create GET request,HOST
pattern_reply_1 = re.compile(r'\s(.*)$')                                   #response CODE (Status = 302/301/200/...)
pattern_location_1 = re.compile(r'^Location:\s(.*)$')                      #target URL


#with open(log, 'a+') as f:                                                 #open log file
for line in foo.content:   
    try:
        if re.search(pattern_send, line):           #read line by line from foo.content (redirected sys.stdout)
            _host = pattern_send_1.search(line).group(2)[:-4]              #[:-4] to del
            _rest = pattern_send_1.search(line).group(1)
            #print >>f, '\nGET: ', _host, _rest                #if NO LOGGER, this print "trick" can be used ;)
            print '\nGET: ', ''.join(_host+_rest)              #www.volvopenta.com / --> www.volvopenta.com/
        elif re.search(pattern_reply, line):
            _status = pattern_reply_1.search(line).group(1)[:-5]
            print '|\n|STATUS: ', _status
        elif re.search(pattern_location, line):
            _target = pattern_location_1.search(line).group(1)
            print '|\n|--->TO: ', _target, '\n','#'*50
        else:
            pass
    except AttributeError,e:                                    #AttributeError is thrown, when no MATCH for 
        pass                                                #re.search - it means there are no redirection!
    
    
    
    
#===========================================================================
# rm = ['fileno','fp','headers','next','read','readlines',\
#         'readline','__iter__']
# new_dict = {}
# for key in f.__dict__.iterkeys():
#   if key not in rm:
#       new_dict[key]= f.__dict__[key]
#
#pprint.pprint(new_dict)   
#===========================================================================
     
#===========================================================================
# myList = [(item,f.__dict__[item]) for item in f.__dict__.keys()\
#           if re.match(r'^_[^_]|code|Date|url', item)]
# pprint.pprint(myList)
# with open("redirect.log", "w+") as f_obj:
#    f_obj.write(str(myList))
#===========================================================================
#r'^_[^_]|code|url' ---> OK: _302_URL, NOTOK: __302_URL'
#match words that starts from only one underscore - second char 
#cannot be underscore [^_]

    
    