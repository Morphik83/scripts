#>MASTER changes

import urllib2

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
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
        #result.URL_1 = [headers[h] for h in headers.keys() if h == 'location']
        result._301_TO_URL = headers.getheader('location')
        result._301_STATUS = code
        result._301_FROM_REQUEST_GET_FULL_URL = req.get_full_url()
        result._301_DATE = headers.getheader('date')
        return result
    
    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
        #result.URL_2 = [headers[h] for h in headers.keys() if h == 'location']
        result._302_TO_URL = headers.getheader('location')
        result._302_STATUS = code
        result._302_FROM_REQUEST_GET_FULL_URL = req.get_full_url()
        result._302_DATE = headers.getheader('date')
        #result._302_TIMESTAMP = time.strftime("%b %d %Y %H:%M:%S")
        return result

if __name__ == '__main__':
    import pprint
    import re
    
    srh = SmartRedirectHandler()
    #handler = urllib2.HTTPHandler()
    #handler.set_http_debuglevel(1)
    opener = urllib2.build_opener(srh)
    #opener.handle_open['http'][0].set_http_debuglevel(1)
    request = urllib2.Request('http://www.volvopenta.com')
    f = opener.open(request)
        
    pprint.pprint(f.__dict__)
    
    #->NEW BRANCH?
    
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
        
        