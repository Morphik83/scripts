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
    opener.handle_open['http'][0].set_http_debuglevel(1)
    request = urllib2.Request('http://www.volvopenta.com')
    f = opener.open(request)
        
    pprint.pprint(f.__dict__)
    
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
        
        
#===============================================================================
#    example output:
# send: 'GET / HTTP/1.1\r\nAccept-Encoding: identity\r\nHost: www.volvopenta.com\r\nConnection: close\r\nUser-Agent: Python-urllib/2.7\r\n\r\n'
# reply: 'HTTP/1.1 301 Moved Permanently\r\n'
# header: Server: Microsoft-IIS/6.0
# header: Content-Type: text/html
# header: Content-Length: 197
# header: Location: http://www.volvopenta.com/volvopenta/splash/en-gb
# header: Expires: Wed, 14 Nov 2012 18:44:50 GMT
# header: Cache-Control: max-age=0, no-cache, no-store
# header: Pragma: no-cache
# header: Date: Wed, 14 Nov 2012 18:44:50 GMT
# header: Connection: close
# send: 'GET /volvopenta/splash/en-gb HTTP/1.1\r\nAccept-Encoding: identity\r\nHost: www.volvopenta.com\r\nConnection: close\r\nUser-Agent: Python-urllib/2.7\r\n\r\n'
# reply: 'HTTP/1.1 302 Moved Temporarily\r\n'
# header: Content-Length: 197
# header: Content-Type: text/html
# header: Location: http://www.volvopenta.com/volvopenta/splash/en-gb/Pages/global_splash.aspx
# header: Server: Microsoft-IIS/6.0
# header: Server: SEGOTN2544
# header: X-Powered-By: ASP.NET
# header: Expires: Wed, 14 Nov 2012 18:44:51 GMT
# header: Cache-Control: max-age=0, no-cache, no-store
# header: Pragma: no-cache
# header: Date: Wed, 14 Nov 2012 18:44:51 GMT
# header: Connection: close
# send: 'GET /volvopenta/splash/en-gb/Pages/global_splash.aspx HTTP/1.1\r\nAccept-Encoding: identity\r\nHost: www.volvopenta.com\r\nConnection: close\r\nUser-Agent: Python-urllib/2.7\r\n\r\n'
# reply: 'HTTP/1.1 200 OK\r\n'
# header: Server: Microsoft-IIS/6.0
# header: Server: SEGOTN2543
# header: X-Powered-By: ASP.NET
# header: X-AspNet-Version: 2.0.50727
# header: Cache-Control: private
# header: Expires: Wed, 14 Nov 2012 18:56:25 GMT
# header: Content-Type: text/html; charset=utf-8
# header: Vary: Accept-Encoding
# header: Date: Wed, 14 Nov 2012 18:44:51 GMT
# header: Transfer-Encoding:  chunked
# header: Connection: close
# header: Connection: Transfer-Encoding
# {'_301_DATE': 'Wed, 14 Nov 2012 18:44:50 GMT',
# '_301_FROM_REQUEST_GET_FULL_URL': 'http://www.volvopenta.com',
# '_301_STATUS': 301,
# '_301_TO_URL': 'http://www.volvopenta.com/volvopenta/splash/en-gb',
# '_302_DATE': 'Wed, 14 Nov 2012 18:44:51 GMT',
# '_302_FROM_REQUEST_GET_FULL_URL': 'http://www.volvopenta.com/volvopenta/splash/en-gb',
# '_302_STATUS': 302,
# '_302_TO_URL': 'http://www.volvopenta.com/volvopenta/splash/en-gb/Pages/global_splash.aspx',
# '__iter__': <bound method _fileobject.__iter__ of <socket._fileobject object at 0x7f5a5228de50>>,
# 'code': 200,
# 'fileno': <bound method _fileobject.fileno of <socket._fileobject object at 0x7f5a5228de50>>,
# 'fp': <socket._fileobject object at 0x7f5a5228de50>,
# 'headers': <httplib.HTTPMessage instance at 0x7f5a50375050>,
# 'msg': 'OK',
# 'next': <bound method _fileobject.next of <socket._fileobject object at 0x7f5a5228de50>>,
# 'read': <bound method _fileobject.read of <socket._fileobject object at 0x7f5a5228de50>>,
# 'readline': <bound method _fileobject.readline of <socket._fileobject object at 0x7f5a5228de50>>,
# 'readlines': <bound method _fileobject.readlines of <socket._fileobject object at 0x7f5a5228de50>>,
# 'url': 'http://www.volvopenta.com/volvopenta/splash/en-gb/Pages/global_splash.aspx'}
# [('code', 200),
# ('_302_TO_URL',
#  'http://www.volvopenta.com/volvopenta/splash/en-gb/Pages/global_splash.aspx'),
# ('_301_FROM_REQUEST_GET_FULL_URL', 'http://www.volvopenta.com'),
# ('_302_FROM_REQUEST_GET_FULL_URL',
#  'http://www.volvopenta.com/volvopenta/splash/en-gb'),
# ('_301_STATUS', 301),
# ('url',
#  'http://www.volvopenta.com/volvopenta/splash/en-gb/Pages/global_splash.aspx'),
# ('_302_DATE', 'Wed, 14 Nov 2012 18:44:51 GMT'),
# ('_301_DATE', 'Wed, 14 Nov 2012 18:44:50 GMT'),
# ('_301_TO_URL', 'http://www.volvopenta.com/volvopenta/splash/en-gb'),
# ('_302_STATUS', 302)]
#===============================================================================
    