import urllib2
import loggers

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    """this is were description for the class should go"""
        
    def http_error_default(self, req, fp, code, msg, hdrs):
        """urllib2 searches for http_error_default when error code 304 is thrown

        in original urllib2.HTTPErrorHandler, method http_error_default throws 
        exception - this method overwrites this behavior
        """
        result = urllib2.HTTPError(req.get_full_url(), code, msg, hdrs, 
         fp)
        result.status = code
        return result
    
class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    
    def __init__(self,log):
        sys.stdout = loggers.Logger(log)
        
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
        #result.URL_1 = [headers[h] for h in headers.keys() if h == 'location']
        result._FROM = req.get_full_url()
        result._TO = headers.getheader('location')
        result._STATUS = code
        result._DATE = headers.getheader('date')
        #result._301_header = headers.items()
        result._msg = msg
        
        
        print 'FROM: ',result._FROM, '\n\t\t\t|\n\t\t\t|', result._STATUS,result._msg, '\n\t\t\t|\n\t\t\t--->', result._TO
        #sys.stdout = sys.__stdout__
       
        return result
    
    def http_error_302(self, req, fp, code, msg, headers):
        
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
        #result.URL_2 = [headers[h] for h in headers.keys() if h == 'location']
        result._FROM = req.get_full_url()
        result._TO = headers.getheader ('location')
        result._STATUS = code
        result._DATE = headers.getheader('date')
        #result._302_header = headers.items()
        result._msg = msg
        
     
        print 'FROM: ',result._FROM, '\n\t\t\t|\n\t\t\t|', result._STATUS,result._msg, '\n\t\t\t|\n\t\t\t--->', result._TO 
        #sys.stdout = sys.__stdout__
        
        return result
    

if __name__ == '__main__':

    """"
    ToDo:
    -unify all the returned headers (the same name!)
    -add logging 
    -add graph to make analyzing results easier 
    -parallelly write to std.out and log
    """
    log='D:\\tmp\\xxxxxx.log'
    #>MASTER changes + BRANCH changes

    import pprint
    import re
    import sys
    import loggers
    import time

    #srh = SmartRedirectHandler(log)
    #handler = urllib2.HTTPHandler()
    #handler.set_http_debuglevel(1)
    opener = urllib2.build_opener()
    opener.handle_open['http'][0].set_http_debuglevel(1)
    request = urllib2.Request('http://www.volvopenta.com')
    try:
         opener.open(request)
         #open log file

         #pprint.pprint(f.__dict__)
    except Exception, e:
        print "There was a problem with opening URL. Error: ",e
    finally:
        sys.stdout = sys.__stdout__
        print "This part is executed ALWAYS!"

    
    pattern_send = re.compile(r'^send.*$')
    pattern_reply = re.compile(r'^reply.*$')
    pattern_location = re.compile(r'\bLocation\b.*$')
    
    #phonePattern = re.compile(r'^(\d{3})-(\d{3})-(\d{4})$')
    #print phonePattern.search('800-555-900a0').groups()
    f = open(log, 'r+')
    for line in f:
        if re.search(pattern_send, line):
            print line
        elif re.search(pattern_reply, line):
            print line
        elif re.search(pattern_location, line):
            print line
        else:
            pass
        #get 'send/reply/location/ - parse!
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
    
        
        