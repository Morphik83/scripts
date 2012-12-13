import pprint
import re
import sys
import time
import urllib2
import loggers
from urllib2 import URLError
from config_file import *


"""
ToDo:
-different output types (xml,txt??)
"""
    
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
        out_dict = {}                                   #dict to save all the pairs (origin_url: target_url)
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
        pattern_start_request = re.compile(r'^>>>>ORIGIN_URL:(.*)$')               #this is printed to output in redirect_Runner (for each URL from url_list)
        
        #with open(log, 'a+') as f:                                                 #open log file
        try:
          for line in self.response:                                        #read line by line from foo.content (redirected sys.stdout
              try:
                  if re.search(pattern_start_request, line):
                        print "index: ",self.response.index(line)
                        _origin_url = re.search(pattern_start_request,line)
                        out_list = []           #anytime "index" is changed, new out_list is created
                                                #but out_dict stays the same! out_dict={_origin_url:out_list, _origin_url:out_list,...}
                  elif re.search(pattern_send, line):           
                      _host = pattern_send_1.search(line).group(2)[:-4]              #[:-4] to del \n\r
                      _rest = pattern_send_1.search(line).group(1)
                      #print >>f, '\nGET: ', _host, _rest                #if NO LOGGER, this print "trick" can be used to write to file ;)
                      print '\nGET: ', ''.join(_host+_rest)              #www.volvopenta.com / --> www.volvopenta.com/
                  elif re.search(pattern_reply, line):
                      _status = pattern_reply_1.search(line).group(1)[:-5]
                      print '|\n|STATUS: ', _status
                      if re.match(r'\b200\b', _status):                   #if STATUS = 200, draw #*50 -> redirect reached final url
                          print '\n','#'*50
                  elif re.search(pattern_location, line):
                      _target = pattern_location_1.search(line).group(1)
                      _target = re.sub(r'\b\s\b','%20',_target)           #replace in url: /Home page.aspx' with /Home%20page.aspx'
                     
                      print '|\n|--->TO: ', _target
                      out_list.append(_target[:-1])                       #out_list: list of all the URLs that ORIGIN is redirected TO
                      out_dict[_origin_url.group(1)]=out_list
                      """
                      example output:
                      {'http://www.volvobuses.com': 
                              ['http://www.volvobuses.com/bus/global/en-gb',
                               'http://www.volvobuses.com/bus/global/en-gb/Pages/home_new.aspx'],}    
                      """
                      
                  elif re.search(pattern_error, line):
                      print '\n|', line, '\n\n','#'*50
                  else:
                      pass
              except AttributeError,e:                                    #AttributeError is thrown, when no MATCH for 
                  pass                                                #re.search - it means there are no redirection!
        finally:
            sys.stdout = sys.__stdout__                                 #reset sys.stdout to normal state! Deletes redirection to logger
            pprint.pprint(out_dict)
            
        return out_dict
            
    def verify_redirects(self, redirects_list, out_dict, format=None):
        """
        Function checks if url_2 from input_file is in list of urls generated by
        generate_output funcion.
        
        Input: 
        1.redirects_list => output from input_data(input_file)
        2.out_dict => output from generate_output
        3.format => (XLS/LOG) if None, XLS will be generated by default
        
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
        
        generate_report = getattr(self, "_generate_%s" % format, self._generate_XLS)
        
        generate_report(redirects_list, out_dict)
        
        
    def _generate_XLS(self, redirects_list, out_dict):
        try:
            import xlwt
        except ImportError, e:
            print "Install python module 'xlwt' first!\n",e
            
        #create xls object
        book = xlwt.Workbook(encoding="utf-8") 
        sheet1 = book.add_sheet("Redirects Report")
        
        #define styles
        style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on')
        style1 = xlwt.easyxf('font: name Times New Roman, color-index black, bold off',num_format_str='#,##0.00')
        
        #style for ERROR results (red background)
        err_st = xlwt.easyxf('pattern: pattern solid')
        err_st.pattern.pattern_fore_colour = 2 #RED
        
        #style for OK results (green background)
        ok_st = xlwt.easyxf('pattern: pattern solid')
        ok_st.pattern.pattern_fore_colour = 3 #GREEN
        
        #set column's width (256 * no.of chars)
        sheet1.col(0).width = 256 * 40
        sheet1.col(1).width = 256 * 100
        sheet1.col(2).width = 256 * 8
        
        #sheet1.write(row_number, col_number, "WRITE HERE STH", set_style)
        sheet1.write(0,0,"FROM",style0 )
        sheet1.write(0,1,"FROM",style0 )
        sheet1.write(0,2,"RESULT",style0 )
        
        #start counters
        row = 1
        col = 0  
    
        #iterate over dict.keys() (origin URLs from input_file)
        for url_key in redirects_list[2].keys():        #loop over dict (redirects_list[2], see @redirect_Runner
            #if out_dict has the same key (=the same ORIGIN url):
            if out_dict.has_key(url_key):
                """
                redirects_list[2][url_key] => value (TARGET url from input_file)           
                out_dict[url_key] => out_dict[key] returns list of all the urls that target_url was redirected to
                Below lines check if: out_dict[key] list HAS target_url from input file
                """
                sheet1.write(row,col,url_key,style1 )
                sheet1.write(row, col+1, redirects_list[2][url_key], style1 )
                #strip() added - sometimes there is extra whitespace char at the end
                if redirects_list[2][url_key].strip() in out_dict[url_key]:
                    #if OK, use GREEN background in xls report
                    sheet1.write(row, col+2, str(redirects_list[2][url_key].strip() in out_dict[url_key]), ok_st)
                else:
                    #if NOT OK, use RED background
                    sheet1.write(row, col+2, str(redirects_list[2][url_key].strip() in out_dict[url_key]), err_st)
                #go to the next row
                row=row+1
        book.save(xls_report)
    
    
    def _generate_LOG(self, redirects_list, out_dict):
        with open(final_log, 'a+') as f:
            for url_key in redirects_list[2].keys():
                if out_dict.has_key(url_key):
                    f.write("From: %s \n" % url_key)
                    f.write("To:   %s \n" % redirects_list[2][url_key])
                    f.write("%s\n" % str(redirects_list[2][url_key].strip() in out_dict[url_key]))
                    f.write(50*"-"+"\n")
        

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

    
    
