#!/usr/bin/env python
import pprint
import re
import sys
from loggers import Logger
import time
import urllib2
from urllib2 import URLError

"""
ToDo:
-different output types (xml,txt??)
"""
    
class Output_Parser(Logger):
    """OUTPUT PARSER - input: Logger.content list -> (response)
    
    response = opener.open(request)
    """
    
    """
    by creating instance of the 'Logger' class, we automatically redirect sys.stdout to self.log
    """
    def __init__(self, response, log):
        self.response = response           #logger.content list
        self.log = log                      #log file, when redirects will be displayed in graphical way
        self.logger = Logger(self.log)  
        sys.stdout = self.logger
        
    def generate_output(self):
        """
        in the original response (response = opener.open(request)) among other, there are following tags:
            send: 'GET / HTTP/1.1\r\nAccept-Encoding: identity\r\nHost: www.volvopenta.com\r\nConnection: close\r\nUser-Agent: Python-urllib/2.7\r\n\r\n'
            reply: 'HTTP/1.1 301 Moved Permanently\r\n'
            (...)
            header: Location: http://www.volvopenta.com/volvopenta/splash/en-gb
            (...)
        regex patterns are used to make sure that proper line was selected (GET/HEAD/Location) 
        """
        pattern_send = re.compile(r'^\'GET.*$')          #prepare regexp patterns 
        pattern_reply = re.compile(r'^\'HTTP.*$')
        pattern_location = re.compile(r'\bLocation\b.*$')
        pattern_error = re.compile(r'ERROR\:')          #sometimes open.opener(request) returns <urlopen error [Errno 11004] getaddrinfo failed> 
                                                        #when URL is not valid - this is caught by try: (URLError) and logged.
        
        """
        when proper line is already selected, next step is to extract relevant info, like:
        -HOST, URL used to create GET request,
        -response CODE (Status = 302/301/200/...)
        -target URL 
        """
        pattern_send_1 = re.compile(r'^\'GET\s(.*)\sHTTP.*Host:\s(.*)Connection')  #URL used to create GET request, HOST
        pattern_reply_1 = re.compile(r'\s(.*)$')                                   #response CODE (Status = 302/301/200/...)
        pattern_location_1 = re.compile(r'^Location:\s(.*)$')                      #target URL
        
        #with open(log, 'a+') as f:                                                 #open log file
        try:
          for line in self.response:                                        #read line by line from foo.content (redirected sys.stdout
              try:
                  if re.search(pattern_send, line):           
                      _host = pattern_send_1.search(line).group(2)[:-4]              #[:-4] to del \n\r
                      _rest = pattern_send_1.search(line).group(1)
                      #print >>f, '\nGET: ', _host, _rest                #if NO LOGGER, this print "trick" can be used to write to file ;)
                      print '\nGET: ', ''.join(_host+_rest)              #www.volvopenta.com / --> www.volvopenta.com/
                  elif re.search(pattern_reply, line):
                      _status = pattern_reply_1.search(line).group(1)[:-5]
                      print '|\n|STATUS: ', _status
                      if re.match(r'\b200\b', _status):                   #if STATUS = 200, draw #*50 -> redirect reached final url
                          print "ASSERT:"
                          print '\n','#'*50
                  elif re.search(pattern_location, line):
                      _target = pattern_location_1.search(line).group(1)
                      print '|\n|--->TO: ', _target
                  elif re.search(pattern_error, line):
                      print '\n|', line, '\n\n','#'*50
                  else:
                      pass
              except AttributeError,e:                                    #AttributeError is thrown, when no MATCH for 
                  pass                                                #re.search - it means there are no redirection!
        finally:
          sys.stdout = sys.__stdout__                                 #reset sys.stdout to normal state! Deletes redirection to logger
            

if __name__ == '__main__':
    import loggers
    import sys
    import urllib2
    
    foo = loggers.Logger()   #redirect all the outputs to the foo 
    sys.stdout = foo
    
    url_list = ['http://volvopenta.com', 'http://volvobuses.com', 'http://volvoit.com', 
                'http://volvo.com', 'http://volvotruscks.com', 'http://volvotrucks.com'] 
    try:
        
        for url in url_list:    
            #srh = SmartRedirectHandler(log)        #redirect handler with extra headers
            #handler = urllib2.HTTPHandler()
            #handler.set_http_debuglevel(1)
            opener = urllib2.build_opener()
            opener.handle_open['http'][0].set_http_debuglevel(1)
            request = urllib2.Request(url)
            try:
                opener.open(request)
            except URLError,e:
                print "ERROR: "+url+" This URL does not exist! " + str(e)
            except ValueError, e:
                if re.search(r'unknown url type', str(e)):
                    try:
                        request = urllib2.Request('http://'+url)
                        opener.open(request)
                    except URLError,e:
                        print "ERROR: "+url+" This URL does not exist! " + str(e)
                
    finally:
        sys.stdout = sys.__stdout__
        
    log='D:\\tmp\\xxxxxx.log'       #detailed final log file
    parser = Output_Parser(foo.content, log)
    parser.generate_output()    
        
        
        
        
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

    
    