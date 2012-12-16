import urllib2, urlparse, socket 
import os,sys
import re
import pprint
from config_file import *
from urllib2 import URLError
try:
    import xlwt
except ImportError, e:
    print "Install 'xlwt' - python module for 'xls' file handling!\n",e

#TODO: iteratively substitute original system's host file with server-oriented host files

class Report(object):
    
    def __init__(self, format, report_file):
        self.format = format
        self.report_file = report_file
        #create/open log file (based on report_file extension(format))
        self.create_report_object()
          
    def create_report_object(self):
        """by passing specific self.format, corresponding private function is called
        """
        create_report_object = getattr(self, "create_%s" % self.format)
        create_report_object()
       
    def create_XLS(self):
        """returns XLS obj with one sheet
        """
        #create xls object
        self.book = xlwt.Workbook(encoding="utf-8") 
        self.sheet1 = self.book.add_sheet("my_test_sheet")
       
        #define styles
        style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on')
        
        #set columns' width (256 * no.of chars)
        self.sheet1.col(0).width = 256 * 80  #col with URL
        self.sheet1.col(1).width = 256 * 40  #col with IP_ADDRr
        self.sheet1.col(2).width = 256 * 8   #col with RETURN CODE
        
        #sheet1.write(row_number, col_number, "WRITE HERE STH", set_style)
        self.sheet1.write(0,0,"URL",style0 )
        self.sheet1.write(0,1,"IP_ADDR",style0 )
        self.sheet1.write(0,2,"R_CODE",style0 )
        
        #start rows/columns counters 
        self.row = 1 #row=0 is for column's names
        self.col = 0
            
        return self.book,self.sheet1  #return XLS obj
    
    def create_LOG(self):
        """opens and returns log file
        """
        self.report = open(self.report_file, 'a+')
        return self.report

    def write_to_report(self, *args):
        """by passing specific self.format (args[0]), corresponding private function is called
        """
        write_to_report = getattr(self, "write_%s" % args[0])
        args = args[1:] #we do not need self.format any more
        write_to_report(*args)
    
    def write_LOG(self, *args):
        """writes data to LOG report file
        """
        #url is logged always
        self.report.write("URL: %s \n" % args[0])
        #if error occurred, log only info about error
        if args[3]:
            self.report.write("ERROR: %s \n" % args[3])
        #if no error, log ip_addr & r_code
        else:
            self.report.write("IP_ADDR: %s \n" % args[1])
            self.report.write("R_CODE: %s \n" % args[2])
        
        self.report.write(50*"-"+"\n")

    def write_XLS(self, *args):
        """writes data to XLS report file
        """
        #define styles
        style1 = xlwt.easyxf('font: name Times New Roman, color-index black, bold off',num_format_str='#,##0.00')
        #style for RETURN CODE <> 200 (red background)
        err_st = xlwt.easyxf('pattern: pattern solid')
        err_st.pattern.pattern_fore_colour = 2 #RED
        #style for RETURN CODE 200 (green background)
        ok_st = xlwt.easyxf('pattern: pattern solid')
        ok_st.pattern.pattern_fore_colour = 3 #GREEN
        
        #write data to XLS 
        #url is logged always
        self.sheet1.write(self.row, self.col,   args[0], style1)
        #if error occurred, log only info about error (in IP_ADDR col)
        if args[3]:
            self.sheet1.write(self.row, self.col+1, str(args[3]), err_st)
            self.sheet1.write(self.row, self.col+2, '', err_st)
        #if no error, log ip_addr & r_code
        else:
            self.sheet1.write(self.row, self.col+1, args[1], style1)
            self.sheet1.write(self.row, self.col+2, args[2], ok_st)
        
        #========TO DO===============================================================
        # if args[2]=='200':
        #    #if OK, use GREEN background in xls report
        #    self.sheet1.write(row, col+2, args[2], ok_st)
        # else:
        #    #if NOT OK, use RED background
        #    self.sheet1.write(row, col+2, args[2], err_st)
        #=======================================================================
        
        #increase row counter - go to the next row
        self.row=self.row+1
                    
    def save_report(self):
        """by passing specific self.format, corresponding private function is called
        """
        save_report = getattr(self, "save_%s" % self.format)
        save_report()
    
    def save_XLS(self):
        self.book.save(self.report_file)
        print 'XLS saved'
    
    def save_LOG(self):
        self.report.close()
        print 'LOG saved'
        
class Check_URLs(Report):
    
    def __init__(self):
        self.report = report_file
        self.file_with_urls = file_with_urls
        self.list_with_urls = []
        self.headers = headers
        self.format = self.__getFileExt()
        #create Report Object (dependently on given file format)
        Report.__init__(self, self.format, self.report)
        
        #now, we should have access to methods from Report's class 
        #like, write_to_report method
        
    def __getFileExt(self):
        #filename.ext -> pttrn for (ext)
        pttrn = re.compile(r'^.*?\.(.*)$')
        #search for pttrn in report_file
        search = re.search(pttrn, self.report)
        if search:
            ext = search.group(1).upper()
            try:
                assert len(ext) == 3
                assert ext in ext_accept_list
                return ext
            except AssertionError:
                print "Reports' file extension must be 3 chars long!\
                \nFor available report types see ext_accept_list in config_file.py"
                sys.exit()
        else:
            print 'Missing extension for report file in config_file.py! \n(example:CHECK_URLS.xls)'
            sys.exit()
        
    def get_listOf_URLs(self):
        """Valid input file must have following format:
        url_1
        #url_1   #if line starts with '#' -> skip
        """    
        with open(self.file_with_urls, 'r+') as f:
            searchPattern = re.compile(r'(^[^\/#].*$)')  # in reg_exp ? is used for non-greedy search pattern - without ?, first match will cover whole line (up to $) due to .*
            for url in f:
                search = re.search(searchPattern, url)
                if search:
                    if not re.match(r'^http[s]?://',search.group(1)):
                        url = 'http://'+search.group(1)
                    else:
                        url = search.group(1)
                    self.list_with_urls.append(url)
                
        return self.list_with_urls
    
    def hit_server_with_urls(self):
        
        #create list with urls
        self.list_with_urls = self.get_listOf_URLs()
        #prepare request:enable logging
        handler = urllib2.HTTPHandler(debuglevel=1)
        #add cookie handler
        cookie = urllib2.HTTPCookieProcessor()
        #build opener
        opener = urllib2.build_opener(handler, cookie)
        #install opener
        urllib2.install_opener(opener)
        
        for url in self.list_with_urls:
            request = urllib2.Request(url, None, self.headers)
            try:
                response = opener.open(request)
                ip_addr = socket.gethostbyname(urlparse.urlparse(response.geturl()).netloc)
                r_code = response.getcode()
                print '\nURL:',url
                print '\nCode:',r_code
                print '\nIP:',ip_addr
                error =  None
            except URLError,e:
                #if URLError occurs, log info about it to log file, but does not exit
                print "Is this URL:",url," valid?\n",e
                error = e
            finally:
                self.write_to_report(self.format, url, ip_addr, r_code, error)
        self.save_report()
    
def main():
    check = Check_URLs()
    check.hit_server_with_urls()            

if __name__ == '__main__':
    main()
    
    
