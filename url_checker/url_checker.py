import urllib2, urlparse, socket 
import os,sys,re
import pprint
import shutil                       
from urllib2 import URLError
from httplib import InvalidURL
from os import listdir
from os.path import isfile,join
from time import strftime
from config_file import *

try:
    import xlwt
except ImportError, e:
    print "Install 'xlwt' - python module for 'xls' file handling!\n" \
    "http://pypi.python.org/packages/source/x/xlwt/xlwt-0.7.4.tar.gz \n",e
try:
    import mechanize
except ImportError,e:
    print "Install 'mechanize' - programatic webBrowser \n"\
    "http://pypi.python.org/pypi/mechanize/0.2.5 \n",e

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
        args[0]= format
        args[1]= URL
        args[2]= IP_ADDR
        args[3]= R_CODE
        args[4]= ERROR
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
        
        #increase row counter - go to the next row
        self.row=self.row+1
                    
    def save_report(self):
        """by passing specific self.format, corresponding private function is called
        """
        save_report = getattr(self, "save_%s" % self.format)
        save_report()
    
    def save_XLS(self):
        self.book.save(self.report_file)
        print 'XLS saved:',self.report_file
    
    def save_LOG(self):
        self.report.close()
        print 'LOG saved:',self.report_file

class Requests():
    """
    creates Inet and Xnet requests; feeds CheckURLs
    """     
    def __init__(self):
        self.inet_opener = self.inet_request()
        self.xnet_opener = self.xnet_request()
        
    def inet_request(self):
        #prepare request:enable logging
        handler = urllib2.HTTPHandler(debuglevel=1)
        #add cookie handler
        cookie = urllib2.HTTPCookieProcessor()
        #build opener
        opener = urllib2.build_opener(handler, cookie)
        #install opener
        urllib2.install_opener(opener)
        return opener
    
    def xnet_request(self):
        browser = mechanize.Browser()
        browser.set_debug_http(True)
        browser.set_handle_robots(False)
        browser.set_debug_redirects(True)
        browser.set_debug_responses(True)
        browser.addheaders=[mechanize_headers]
        return browser
    
class Check_URLs(Report,Requests):
    
    def __init__(self):
        self.report = report_file
        self.file_with_urls = file_with_urls
        self.headers = headers
        self.xnet_list = []
        self.inet_list = []
        self.error_list = []
        self.lists_with_urls = []
        self.format = self._getFileExt()
        #create Report Object (dependently on given file format)
        Report.__init__(self, self.format, self.report)
        Requests.__init__(self)
                
    def _getFileExt(self):
        #filename.ext -> pttrn for catching file's extension only! (ext)
        pttrn = re.compile(r'^.*?\.(.*)$')
        #search for pttrn in REPORT_NAME
        search = re.search(pttrn, REPORT_NAME)
        if search:
            ext = search.group(1).upper()           #(log -> LOG)
            try:            
                assert len(ext) == 3                #length of the extension == 3
                assert ext in ext_accept_list       #accept only extension from ext_accept_list
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
        [X]url_1
        [I] url_1
        #[X]url_1   #if line starts with '#' -> skip
        """   
        #regexp patterns:
        valid_line_pattern = re.compile(r'(^[^#\s].*$)')
        xnet_pattern = re.compile(r'(^\[X\])\s*([^\s].*)$')
        inet_pattern = re.compile(r'(^\[I\])\s*([^\s].*)$')
           
        with open(self.file_with_urls, 'r+') as opened_file:
           for line in opened_file:
               #print "LINE:",line
               valid_line = re.search(valid_line_pattern, line)
               if valid_line:
                   try:
                       #print re.search(Xnet_Pattern,line).groups()
                       url = re.search(xnet_pattern,line).group(2)
                       if not re.match(r'http[s]?://',url):
                          url = 'http://'+url                   #all the send urls must have 'http://' prefix
                       self.xnet_list.append(url.strip())
                   except AttributeError:                       #if no [X] urls found, check for [I] urls
                       try:                    
                           #print re.search(Inet_Pattern,line).groups()
                           url = re.search(inet_pattern,line).group(2)
                           if not re.match(r'http[s]?://',url):
                              url = 'http://'+url
                           self.inet_list.append(url.strip())
                       except AttributeError,e:                 #if no [X]|[I] are found, then check urls 
                           print 'ERROR: %s check prefix!  e:%s' % (line,e)
                           if line not in self.error_list:  #to avoid appending the same info for each server - log only once
                               self.error_list.append(line)
               
        return self.inet_list, self.xnet_list, self.error_list        #when parsing is done, return 3 lists
    
    def hit_server_with_urls(self):
        #get lists with urls:
        self.get_listOf_URLs()
        for url in self.inet_list:
            request = urllib2.Request(url, None, self.headers)
            try:
                response = self.inet_opener.open(request)
                ip_addr = socket.gethostbyname(urlparse.urlparse(response.geturl()).netloc)
                r_code = response.getcode()
                #print '\nURL:',url
                #print '\nCode:',r_code
                #print '\nIP:',ip_addr
                error =  None
                self.write_to_report(self.format, url, ip_addr, r_code, error)
            except (URLError,InvalidURL),e:
                #if URLError occurs, log info about it to log file, but does not exit
                print "Is this URL:",url," valid?\n",e
                error = e
                self.write_to_report(self.format, url, '', '', error)
        self.inet_list = []      
                
                
        for url in self.xnet_list:
            try:
                r = self.xnet_opener.open(url)
                #print 'HEADERS: \n',b.response().info(), '\nEND HEADERS'
                #print self.xnet_opener.response().code #or alternatively: print r.code 
              
                self.xnet_opener.select_form(nr=0)
                self.xnet_opener["ctl00$BodyContent$login$UserName"]=username
                self.xnet_opener["ctl00$BodyContent$login$Password"]=passwd
                self.xnet_opener.submit(name='ctl00$BodyContent$login$LoginButton')
                #print dir(b)
                #print 'URL:',b.geturl()
                #print 'HEADERS: \n',b.response().info(), '\nEND HEADERS'
                r_code = r.code
                ip_addr = socket.gethostbyname(urlparse.urlparse(r.geturl()).netloc)
                error =  None
                self.write_to_report(self.format, url, ip_addr, r_code, error)
            except mechanize.ControlNotFoundError,e:
                """
                ControlNotFoundError occurs when no Login/Pass forms are located on the page -> it might be that 
                the user is already logged in, so that is why the return code (200) is checked. 
                """
                try:
                    assert r.code == 200
                    print 'Return Code is 200'
                    ip_addr = socket.gethostbyname(urlparse.urlparse(r.geturl()).netloc)
                    r_code = r.code
                    error = None
                    self.write_to_report(self.format, url, ip_addr, r_code, error)
                except AssertionError,e:
                    print 'Return code is not 200! It is: ',e
                    error = e
                    self.write_to_report(self.format, url, '', '', error)
                    
            except (NameError,mechanize.FormNotFoundError),e:
                print 'FIXME:',url,e
                error = e
                self.write_to_report(self.format, url, '', '', error)
            except (URLError,InvalidURL),e:
                    #if URLError occurs, log info about it to log file, but does not exit
                    print "Is this URL:",url," valid?\n",e
                    error = e
                    self.write_to_report(self.format, url, '', '', error)
                    
        self.xnet_list = []
        self.xnet_opener.clear_history()       
        print 'This URLs were not verified (= are not included in the report): ',self.error_list
    
class Run_URL_Checks_OnServers(Check_URLs):
    '''
    content of the /etc:
    >>>>
    AKAMAI
    SEGOTN2525 
    SEGOTN2543
    SEGOTN2553
    SEGOTN2544
    hosts
    <<<<
    
    1.rename host_original -> host_backUp
    2.iteratively rename SEGOTNXXXX -> host_original
        3.run URL checks
        4.rename-back host_original -> SEGOTNXXXX
    5.When all servers checked, rename host_backUp -> host_original 
    '''
    
    def __init__(self):
        #list all the files from PATH_HOSTS (~/etc dir)
        self.all_files = [f for f in listdir(PATH_HOSTS) if isfile(join(PATH_HOSTS,f))]
        self.end = False
        #create instance of the Check_URLs class
        Check_URLs.__init__(self)
        
    def backUp_originalHost(self):
        #backup original host file
        #find host file
        if host_original in self.all_files:
            try:
                #create backUp of the original host file (rename)
                os.rename(os.path.join(PATH_HOSTS,host_original), os.path.join(PATH_HOSTS,host_backUp))
                print 'BackUp of the original HOST file: host-> %s' % host_backUp
                return True
            except WindowsError,e:
                print '%s already exists!, \n%s' %(os.path.join(PATH_HOSTS,host_backUp),e)
                return False
        else: 
            print 'Original host file not found in "%s"' % (PATH_HOSTS)
            return False
             
    def setServerHostFile_and_RunUrlChecks(self):
        #search for Server-Oriented host files:
        #server_hosts_pattern defined in config_file.py
        print "setServerHostFile_and_RunUrlChecks:self.all_files:",self.all_files
        for host_Server in self.all_files:
            if re.search(server_hosts_pattern, host_Server):
                print 'using host_Server:',host_Server
                self.write_to_report(self.format,"Host_Server:",host_Server,"####","")
                #rename Server-Oriented host to Windows-Oriented host (SEGOTN2525 to host)
                os.rename(os.path.join(PATH_HOSTS,host_Server), os.path.join(PATH_HOSTS,host_original))
                #EXECUTE URL CHECKS
                self.hit_server_with_urls()
                self.write_to_report(self.format,"","","","") 
                
                #when checking is done, revert Windows-Oriented host to Server-Oriented host (host to SEGOTN2525)
                os.rename(os.path.join(PATH_HOSTS,host_original), os.path.join(PATH_HOSTS,host_Server))
                print '-->next....'
        #when all the host_Server's file used, revert original host file       
        self.end = True
        self.save_report()
        
    def set_OriginalHost(self):
        
        #if self.end is True, revert host to original file
        if self.end:
            #get list of all the files in PATH_HOSTS
            files = [f for f in listdir(PATH_HOSTS) if isfile(join(PATH_HOSTS,f))]
            if host_backUp in files:
                print "renaming host_backUp to original hosts file"
                os.rename(os.path.join(PATH_HOSTS, host_backUp), os.path.join(PATH_HOSTS,host_original))
        else:
            print 'Problem with setting original host!'
       
        
def main():
    #check = Check_URLs()
    #check.hit_server_with_urls()
    obj = Run_URL_Checks_OnServers()

    if obj.backUp_originalHost():
       obj.setServerHostFile_and_RunUrlChecks()
    obj.set_OriginalHost()

    
    
if __name__ == '__main__':
    main()

    
    
    
    
    
    
       
       
       
       
       
       
       