import pprint
import re
import sys
import time
import urllib2
import loggers
from urllib2 import URLError
from config_file import *

class Output_Parser(loggers.Logger):
    """Output_Parser - input: Logger.content list -> (response)
    
    response = opener.open(request)
    """
    
    """
    by creating instance of the 'Logger' class, we automatically redirect sys.stdout to self.log
    """
    def __init__(self, response, log):
        self.response = response            #logger.content list 
        self.log = log                      #graphic_log file
        self.logger = loggers.Logger(self.log)  
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
        
        """
        select proper line and extract relevant info, like:
        -HOST, URL used to create GET request,
        -response CODE (Status = 302/301/200/...)
        -target URL 
        """
        #dict to save all the pairs (origin_url: target_url)
        out_dict = {}                                                            
        #URL used to create GET request, HOST
        pttrn_send = re.compile(r'^\'GET\s(.*)\sHTTP.*Host:\s(.*)Connection')  
        #response CODE (Status = 302/301/200/...)
        pttrn_reply = re.compile(r'^\'HTTP.*?\s(.*)$')                         
        #target URL
        pttrn_location = re.compile(r'^Location:\s(.*)$')                      
        #this is printed to output in redirect_Runner (for each URL from url_list)
        pttrn_start_request = re.compile(r'^>>>>ORIGIN_URL:(.*)$')             
        #sometimes open.opener(request) returns <urlopen error [Errno 11004] getaddrinfo failed>
        #when URL is not valid - this is caught by try: (URLError) and logged.
        pttrn_error = re.compile(r'ERROR\:')                                    
                                                                                 
        try:
          #read line by line from foo.content (redirected sys.stdout)
          for line in self.response:
              try:
                  if re.search(pttrn_start_request, line):
                      print '#'*50
                      print "index: ",self.response.index(line)
                      _origin_url = re.search(pttrn_start_request,line)
                      out_list = []           #anytime "index" is changed, new out_list is created
                                              #but out_dict stays the same! out_dict={_origin_url:out_list, _origin_url:out_list,...}
                  elif re.search(pttrn_send, line):           
                      _host = pttrn_send.search(line).group(2)[:-4]            #[:-4] to del \n\r
                      _rest = pttrn_send.search(line).group(1)
                      #print >>f, '\nGET: ', _host, _rest                        #if NO LOGGER, this print "trick" can be used to write to file ;)
                      print '\nGET: ', ''.join(_host+_rest)                      #www.volvopenta.com / --> www.volvopenta.com/
                      #print '\nGET: ', ''.join(_rest)                      #www.volvopenta.com / --> www.volvopenta.com/
                                            
                  elif re.search(pttrn_reply, line):
                      _status = pttrn_reply.search(line).group(1)[:-5]
                      print '|\n|STATUS: ', _status
                      http_response = [r'400 Bad Request',r'403 Forbidden',\
                                       r'404 Not Found',r'405 Method Not Allowed',\
                                       r'406 Method Not Allowed',\
                                       r'407 Proxy Authentication Required',\
                                       r'408 Request Timeout',\
                                       r'409 Conflict',r'410 Gone',\
                                       r'411 Length Required',\
                                       r'412 Precondition Failed',\
                                       r'413 Request Entity Too Large',\
                                       r'414 Request-URI Too Long',\
                                       r'415 Unsupported Media Type',\
                                       r'416 Requested Range Not Satisfiable',\
                                       r'417 Expectation Failed',\
                                       r'500 Internal Server Error',\
                                       r'501 Not Implemented',\
                                       r'502 Bad Gateway',\
                                       r'503 Service Unavailable',\
                                       r'504 Gateway Timeout',\
                                       r'505 HTTP Version Not Supported',\
                                       r'200 OK']
                      #cannot add to http_response r'401 Unauthorized'-usually it's correct redirect  
                      for item in http_response:
                          if not out_list:                          #add status if out_list is empty
                              if re.search(item, _status):
                                  out_dict[_origin_url.group(1)]=_status
                          
                                      
                  elif re.search(pttrn_location, line):
                      _target = pttrn_location.search(line).group(1)
                      _target = re.sub(r'\b\s\b','%20',_target)                  #replace in url: /Home page.aspx' with /Home%20page.aspx'
                     
                      print '|\n|--->TO: ', _target
                      out_list.append(_target[:-1])                              #out_list: list of all the URLs that ORIGIN is redirected TO
                      out_dict[_origin_url.group(1)]=out_list
                      """
                      example output:
                      {'http://www.volvobuses.com': 
                              ['http://www.volvobuses.com/bus/global/en-gb',
                               'http://www.volvobuses.com/bus/global/en-gb/Pages/home_new.aspx'],}    
                      """
                  elif re.search(pttrn_error, line):
                      print '\n|', line, '\n\n'
                      if not out_list:                          #add error if out_list is empty
                          out_dict[_origin_url.group(1)]='ERROR!'
                      
                                                
              except AttributeError,e:                                           #AttributeError is thrown, when no MATCH for 
                  pass                                                           #re.search - it means there are no redirection!
        finally:
            print '#'*50,'\nAll redirects:\n'
            pprint.pprint(out_dict)
            sys.stdout = sys.__stdout__                                          #reset sys.stdout to normal state! Deletes redirection to logger
            print '\nDONE!\n'
            
        return out_dict
            
    def verify_redirects(self, redirects_list, out_dict, format=None):
        """
        Function checks if url_2 from input_file is in list of urls generated by
        generate_output function.
        
        Input: 
        1.redirects_list => output from input_data(input_file)
        2.out_dict => output from generate_output
        3.format => (XLS/LOG), if None, XLS will be generated by default
        
        So, for example:
        redirects_list[2]:
        {'http://www.volvobuses.com' : 'http://www.volvobuses.com/bus/global/en-gb/Pages/home_new.aspx'}
        
        out_dict:
        {'http://www.volvobuses.com': 
                 ['http://www.volvobuses.com/bus/global/en-gb',
                  'http://www.volvobuses.com/bus/global/en-gb/Pages/home_new.aspx'],}
        Check if (value IN list):
        redirects_list[2]['http://www.volvobuses.com'] IN out_dict['http://www.volvobuses.com'] => TRUE/FALSE
        """
        
        generate_report = getattr(self, "_generate_%s" % format.upper(), self._generate_XLS)
        
        generate_report(redirects_list, out_dict)
        
        
    def _generate_XLS(self, redirects_list, out_dict):
        try:
            import xlwt
        except ImportError, e:
            print "Install python module 'xlwt' first!\n",e
            
        #create xls object
        book = xlwt.Workbook(encoding="utf-8") 
        sheet1 = book.add_sheet("Redirects Report")
        
        f_1 = xlwt.Font()
        f_1.name = 'Verdana'
        #f.bold = True
        f_1.underline = xlwt.Font.UNDERLINE_SINGLE
        f_1.colour_index = 4
        
        #define styles
        style0 = xlwt.easyxf('font: name Verdana, color-index black, bold on')  #columns styles
        style1 = xlwt.easyxf('font: name Verdana, color-index black, bold off',num_format_str='#,##0.00') 
        style2 = xlwt.easyxf()
        style2.font = f_1        
        
        #style for ERROR results (red background)
        err_st = xlwt.easyxf('pattern: pattern solid')
        err_st.pattern.pattern_fore_colour = 2 #RED
        
        #style for OK results (green background)
        ok_st = xlwt.easyxf('pattern: pattern solid')
        ok_st.pattern.pattern_fore_colour = 3 #GREEN
        
        #set column's width (256 * no.of chars)
        sheet1.col(0).width = 256 * 40
        sheet1.col(1).width = 256 * 100
        sheet1.col(2).width = 256 * 16
        
        #sheet1.write(row_number, col_number, "WRITE HERE STH", set_style)
        sheet1.write(0,0,"FROM",style0 )
        sheet1.write(0,1,"TO",style0 )
        sheet1.write(0,2,"RESULT",style0 )
        
        #start counters
        row = 1
        col = 0  
    
        for x in xrange(len(redirects_list)):        #loop over redirects_list[2], see in redirect_Runner
            """example output:
            redirects_list[0] =>['comment_1', ('url_1', 'url_2')]
            redirects_list[1] =>['comment_2', ('url_3', 'url_4'), ('url_5', 'url_6')]
            """
            for y in xrange(len(redirects_list[x])):
                if y==0:
                    #print 'COMMENTS:',redirects_list[x][y]
                    sheet1.write(row,col,redirects_list[x][y],style0)
                    #go to the next row
                    row=row+1
                else:
                    #print 'FROM:',redirects_list[x][y][0]
                    url_from = redirects_list[x][y][0]  #url_1,url_3,url_5
                    #print 'TO:',redirects_list[x][y][1]
                    url_to = redirects_list[x][y][1]    #url_2,url_4,url_6
                    if out_dict.has_key(url_from):
                        n="HYPERLINK"   #log url(FROM) as active link
                        sheet1.write_merge(row, row, col, col, xlwt.Formula(n + '("'+url_from+'";"'+url_from+'")'), style2)
                        sheet1.write(row, col+1, url_to, style1 )
                        par = url_to.strip() in out_dict[url_from] #or out_dict[url_from]=='200 OK' #FIX: http://www.volvotrucks.com http://www.volvotrucks.com OK
                        if par:
                           #if OK, use GREEN background in xls report
                           sheet1.write(row, col+2, par, ok_st)
                        else:
                            if not isinstance(out_dict[url_from],basestring): #if out_dict[url_from] not string (so is list with redirects)
                                #if NOT OK, use RED background
                                sheet1.write(row, col+2, par, err_st)
                            else:
                                sheet1.write(row, col+2, out_dict[url_from], err_st) #if out_dict[url_from] is str (so is _status)
                        #go to the next row
                        row=row+1
        book.save(xls_report)
        print xls_report," saved"

if __name__ == '__main__':
    pass
        
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

    
    
