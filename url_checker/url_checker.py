import urllib2
import urlparse
import socket 
import os
import sys
import re
import pprint
import shutil
import time
import win32com.client
import loggers
from _root import RootClass                       
from urllib2 import URLError
from httplib import InvalidURL
from os import listdir
from os.path import isfile,join
from time import strftime
from config_file import *
#import get_PROXY

try:
    import xlwt
except ImportError, e:
    print "Install 'xlwt' - python module for 'xls' file handling!\n" \
    "http://pypi.python.org/packages/source/x/xlwt/xlwt-0.7.4.tar.gz \n",e
try:
    import mechanize
    from mechanize._mechanize import BrowserStateError
except ImportError,e:
    print "Install 'mechanize' - programatic webBrowser \n"\
    "http://pypi.python.org/pypi/mechanize/0.2.5 \n",e

class Report(RootClass,object):
    """initializes Report object
    """
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
        self.sheet1.col(0).width = 256 * 110  #col with URL
        self.sheet1.col(1).width = 256 * 40  #col with IP_ADDRr
        self.sheet1.col(2).width = 256 * 8   #col with RETURN CODE
        #sheet1.write(row_number, col_number, "WRITE HERE STH", set_style)
        self.sheet1.write(0,0,"URL",style0 )
        self.sheet1.write(0,1,"HOST / IP_ADDR",style0 )
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
        #url is always logged 
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
        print '\n'
        self._info('XLS saved:[',self.report_file,']')
    
    def save_LOG(self):
        self.report.close()
        print '\n'
        self._info('LOG saved:',self.report_file)

class Menu(RootClass,object):
    '''simple menu with basic selection of the host files and switcher for 
    verifying all the subpages
    '''
    
    def __init__(self):
        self.production_run = False
        self.qa_run = False
        self.welcome_page()
        self.checklist=[]
        self.get_email_addresses()
        self.menu()
    
    def welcome_page(self):
        self._info('>> CWP_URL_Checker << author: Maciej Balazy >>')
        print (INTRO)
        
    def _get_host_list(self):
        self.host_list = []     
        for host_server in self.all_files:
            if re.search(server_hosts_pattern, host_server):
                self.host_list.append(host_server)
        return self.host_list
    
    def _get_url_list(self):
        url_list = []
        url_QA_list = []
        with open(self.file_with_urls, 'a+') as f:
            for line in f:
                if line.startswith('[X]') or line.startswith('[I]'):
                    url_list.append(line.strip())
                if line.startswith('[X_QA]') or line.startswith('[I_QA]'):
                    url_QA_list.append(line.strip())
        #set global switchers for Prod/QA respectively:
        if url_list:            
            self._info("Production URLs:")    
            pprint.pprint(url_list)
            print
            self.production_run = True
        if url_QA_list:
            self._info("QA URLs:")
            pprint.pprint(url_QA_list)
            print
            self.qa_run = True
        if (not url_list) and (not url_QA_list):
            self._info('URLS.input file is empty!')
            sys.exit()
            
    def get_email_addresses(self):
        addr_to = raw_input('Enter valid e-mail address [to]: ')
        #if re.search(r'[@]',addr_to):
        if re.search(r'\w+@\w+\.\D{3}',addr_to):
            self.to=addr_to
        else:
            self.to=None
            print 'E-mail address not valid! Cannot send e-mail!'
        
        addr_cc = raw_input('Enter valid e-mail address [cc]: ')
        if re.search(r'[@]',addr_cc):
            self.cc=addr_cc
        else:
            self.cc=None
            print 'Ohh come on! Is this really correct e-mail[cc] ? :)'
            
        return self.to,self.cc        
            
    def menu(self):
        def _menu_check_subPages(self):
            """set True/False whether you want to check all the subpages on the given page
            set TRUE  if all the links from given page should be checked as well 
            (eg. http://volovit.com -> any link that exists on that page will be checked) 
            set FALSE if only pages from URLS.input file should be checked
            """
            check = raw_input('\nDo you want to verify sub_pages? [y/n]: ')
            if re.search(r'\b[yY]\b',check):
                self.check_all_subPages = True
                self._info('check_all_subPages: TRUE\n')
                return self.check_all_subPages
            elif re.search(r'\b[nN]\b',check):
                self.check_all_subPages = False
                self._info('check_all_subPages: FALSE\n')
                return self.check_all_subPages
            else:
                self._warn('Not valid answer! Valid: [y/n]\nStarting again...\n')
                _menu_check_subPages(self)
                
        def _menu_add_servers(self):
            def _for_host_server(self):
                for host_server in self.host_list:
                    msg = ''.join(['Add [',host_server,'] to checklist? [y/n]: '])
                    yes_no = raw_input(msg)
                    if re.search(r'\b[yY]\b',yes_no):
                        #del host_server from self.host_list
                        self._info(self.host_list.pop(self.host_list.index(host_server))\
                                   ,' added to current checklist')
                        #print all the still available servers:
                        self._info('Still available/Not used servers: ',self.host_list)
                        #add host_server to current checklist:
                        self.checklist.append(host_server)
                        #print all the servers added to checklist:
                        self._info('Current checklist: ',self.checklist,'\n')
                        #start again 'for' loop with updated self.host_list from the index[0]
                        _for_host_server(self)
                        return
                    elif re.search(r'\b[nN]\b',yes_no):
                        self._info('Skipping [',host_server,']...')
                        #del host_server from self.host_list
                        self.host_list.pop(self.host_list.index(host_server))
                        #print all the still available servers:
                        self._info('Still available/Not used servers: ',self.host_list)
                        #print current checklist:
                        self._info('Current checklist: ',self.checklist,'\n')
                        #start again 'for' loop with updated self.host_list from the index[0]
                        _for_host_server(self)
                        return
                    else:
                        self._warn('Not valid answer! Valid: [y/n]\nStarting again...\n')
                        #erase all the content from self.checklist
                        self.checklist = []
                        _menu_add_servers(self)
                        '''Why do I need 'return' statement in the 'else'?
                        Due to: method call inside method's own body in 'for' loop
                        ->call_1|else:
                                |->call_2|else:
                                         |->call_3->OK|
                                   backTo:Else(call_2)|
                              finish'Else':.return|<--|
                               backTo:Else(call_1)|
                          finish'Else':.return|<--|
                                         OK <-|
                        '''
                        return

            #present all the valid/available HOST files    
            self._info('>>Select servers for checking Production URLs<<')                
            self._info('Reading [%s]' % PATH_HOSTS,'...')
            #any time _menu_add_servers is called - create new list 
            #(avoid appending to already existing list)
            
            if self._get_host_list():
                self._info('Available server-host files: ',self.host_list,'\n')
                resp = raw_input('Add all servers to checklist? [y/n] ')
                if re.search(r'\b[yY]\b|\byes\b|\bYES\b',resp):
                    self._info('Adding all servers to checklist...\n')
                    self.checklist = self.host_list[:]
                elif re.search(r'\b[nN]\b|\bno\b|\bNO\b',resp):
                    self._info('Add servers to checklist:')
                    _for_host_server(self)
                    #return
                else:
                    self._warn('Not valid answer! Valid: [y/n]\nStarting again...\n')
                    _menu_add_servers(self)
                    return
                
            if len(self.checklist)==0:
                self._warn('Current checklist is empty!\nNo servers selected!\nStart again...')
                sys.exit()
            else:
                self._info('Servers to verify [Production URLs only!]:')
                self._info(self.checklist)
        
        try:
            print
            self._info('>>Configuration<<')   
            print
            self._info('URLs to verify -> [%s]' % file_with_urls)
            self._get_url_list()
            
            if self.qa_run:
                self._info('>>QA URLs will be checked using empty hosts file ("QA" in /drivers/etc/)')
                print
            
            #select server_host files
            if self.production_run:
                _menu_add_servers(self)
            
            #sets check_all_subPages=True/False
            _menu_check_subPages(self)
            
            #Startup ?
            self._info('Report file will be saved here: [%s]' %report_file)
            go = raw_input("Run ? [y/n] ")
            if re.search(r'\b[yY]\b|\byes\b|\bYES\b',go):
                pass
            else:
                self._info('Exiting...\n')
                sys.exit()
            
        except KeyboardInterrupt:
            print '\n'
            self._warn('Stopped by user!')
            sys.exit()
        
class Get_Browser(object):
    """
    creates browser's instance; feeds CheckURLs
    """     
    def __init__(self):
        self._opener = self._browser()
  
    def _browser(self):
        browser = mechanize.Browser()
        browser.set_debug_http(True)
        browser.set_handle_robots(False)
        browser.set_debug_redirects(True)
        browser.set_debug_responses(True)
        browser.addheaders=[mechanize_headers]
        return browser
    
class Check_URLs(Report,Get_Browser,Menu):
    """defines methods that create lists with valid URLs, also 'hitsServerWithURLS'
    """
    def __init__(self):
        self.report = report_file
        self.file_with_urls = file_with_urls
        self.xnet_list = []
        self.inet_list = []
        self.qa_xnet_list = []
        self.qa_inet_list = []
        self.error_list = []
        self.skipped_list = []
        self.format = self._getFileExt()
        self.run_proxy = run_URL_checks_through_PROXY
        Report.__init__(self, self.format, self.report)
        if not self.run_proxy:    #TODO: add Proxy handling to Menu 
            Menu.__init__(self) 
                
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
                self._warn("Reports' file extension must be 3 chars long!\
                \nFor available report types see ext_accept_list in config_file.py")
                sys.exit()
        else:
            self._warn('Missing extension for report file in config_file.py! \n(example:CHECK_URLS.xls)')
            sys.exit()
    
    def _get_url_host(self, url):
        parsed = urlparse.urlparse(url)
        if parsed.scheme and parsed.netloc:
            self.url_host = parsed.scheme + '://' + parsed.netloc
            return self.url_host
        else:
            self._warn('_get_url_host: Cannot find hostname in given url! [',url,']')
    
    def get_listOf_URLs(self):
        """Valid input file must have following format:
        [X]url_1, [X_QA] url_2
        [I] url_1, [I_QA] url_2
        #[X]url_1   #if line starts with '#' -> skip
        """   
        #Production regexp patterns:
        valid_line_pattern = re.compile(r'(^[^#\s].*$)')
        xnet_pattern = re.compile(r'(^\[X\])\s*([^\s].*)$')
        inet_pattern = re.compile(r'(^\[I\])\s*([^\s].*)$')
        #QA regexp patterns:
        qa_xnet_pattern = re.compile(r'(^\[X_QA\])\s*([^\s].*)$')
        qa_inet_pattern = re.compile(r'(^\[I_QA\])\s*([^\s].*)$')
           
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
                       except AttributeError:                       #if no [X] and [I], try QA patterns
                           try:
                               url = re.search(qa_xnet_pattern,line).group(2)
                               if not re.match(r'http[s]?://',url):
                                   url = 'http://'+url                   
                               self.qa_xnet_list.append(url.strip())
                           except AttributeError:
                               try:
                                   url = re.search(qa_inet_pattern,line).group(2)
                                   if not re.match(r'http[s]?://',url):
                                      url = 'http://'+url
                                   self.qa_inet_list.append(url.strip())
                               except AttributeError,e:
                                    self._warn('ERROR: %s verify prefix!  e:%s' % (line,e))
        
        return self.inet_list, self.xnet_list, self.qa_inet_list, self.qa_xnet_list       #when parsing is done, return 4 lists
    
    def _check_url_for_error(self, url):
        self.time_out = False
        print '\n'
        errorList = [r'(\w+\sis not available)',\
                     r'(Value does not fall within the expected range)',\
                     r'(Field type CWPRichText is not installed properly)',\
                     r'(at Microsoft.SharePoint.\.*)',\
                     r'(Object reference not set to an instance of an object)',\
                     r'(key was not present)',\
                     r'(Invalid URI: The format of the URI could not be determined)',\
                     r'(Custom404Module)']
        
        response = self._opener.response()
        self._info("Parsing opened page...")
        the_page = response.read()
        
        'check if request timed-out'
        if re.search(r'(Request timed out)', the_page):
            self.time_out = True
            return self.time_out
     
        #print 'chars_onPage:',len(the_page)
        self._info("-->checking [%s] for errors... [page length: %d] " %(url,len(the_page)))
        for error in errorList:
            search = re.search(error, the_page)
            if search:
                self._warn('CHECK THIS URL:\n[%s]\n[%s]!\n' %(url, search.group(1)))
                self.error_list.append([url,search.group(1)])
                self.write_to_report(self.format, url, '', '', search.group(1))
                return #to avoid appending the same url twice if more than one error is discovered on the page
            else:
                self._info('No errors noticed\n')
        
    def hit_production_servers_with_urls(self):
        if self.production_run:
            #self.test_list defined, since _check_url is used for both inet & xnet
            if self.inet_list:
                self.test_list = self.inet_list      
                self.__check_url(self.check_all_subPages, xnet_login=False)
            if self.xnet_list:
                self.test_list = self.xnet_list
                self.__check_url(self.check_all_subPages, xnet_login=True)
            
        #clear lists content:
        self.inet_list = []
        self.xnet_list = []
        self._warn('Check these URLs: ')
        pprint.pprint(self.error_list) 
        self._warn('Skipped URLs: ')
        pprint.pprint(self.skipped_list)   

    def hit_qa_servers_with_urls(self):
        if self.qa_run:
            #self.test_list defined, since __check_url is used for both inet & xnet
            if self.qa_inet_list:
                self.test_list = self.qa_inet_list      
                self.__check_url(self.check_all_subPages, xnet_login=False)
            if self.qa_xnet_list:
                self.test_list = self.qa_xnet_list
                self.__check_url(self.check_all_subPages, xnet_login=True)
            
        #clear lists content:
        self.qa_inet_list = []
        self.qa_xnet_list = []
        self._warn('Check these URLs: ')
        pprint.pprint(self.error_list) 
        self._warn('Skipped URLs: ')
        pprint.pprint(self.skipped_list) 

            
    def __check_url(self, check_all_subPages, xnet_login):
        for url in self.test_list:
            try:    
                if self.run_proxy:
                    self._info('GETTING PROXY...')
                    proxies = get_PROXY.get_proxy_from_pac(pacfile, url)
                    self._opener.set_proxies(proxies)
                self._get_url_host(url)
                self._info('URL_HOST:',self.url_host)
                response = self._opener.open(url)
                #print 'HEADERS: \n',b.response().info(), '\nEND HEADERS'
                #print self.xnet_opener.response().code #or alternatively: print r.code 
                
                if xnet_login:
                    #LOGIN:
                    self._opener.select_form(nr=0)
                    self._opener["ctl00$BodyContent$login$UserName"]=username
                    self._opener["ctl00$BodyContent$login$Password"]=passwd
                    self._opener.submit(name='ctl00$BodyContent$login$LoginButton')
                #print 'HEADERS: \n',b.response().info(), '\nEND HEADERS'
                
                self._check_url_for_error(url)
                #get status:
                r_code = response.code
                if self.run_proxy:
                    ip_addr = proxies['http']
                    self._info("(proxy):",proxies['http'])
                else:
                    ip_addr = socket.gethostbyaddr(urlparse.urlparse(response.geturl()).netloc)
                    ip_addr = str(ip_addr[0])+" / "+str(ip_addr[2][0])
                    self._info("(hostname/aliases/IPlist):",ip_addr)
                #url = r.geturl()
                error = None
                self.write_to_report(self.format, url, ip_addr, r_code, error)
                
                if check_all_subPages:
                    self.__check_all_subPages()
                    
            except mechanize.ControlNotFoundError,error:
                """
                ControlNotFoundError occurs when no Login/Pass forms are located on the page -> it might be that 
                the user is already logged in, so that is why the return code (200) is checked. 
                """
                try:
                    assert response.code == 200
                    self._info('Return Code is 200')
                    #check for error
                    self._check_url_for_error(url)
                    ip_addr = socket.gethostbyaddr(urlparse.urlparse(response.geturl()).netloc)
                    ip_addr = str(ip_addr[0])+" / "+str(ip_addr[2][0])
                    r_code = response.code
                    error = None
                    self.write_to_report(self.format, response.geturl(), ip_addr, r_code, error)
                    if check_all_subPages:
                        self.__check_all_subPages()
                except AssertionError,e:
                    self._warn('Return code is not 200! It is: ',error)
                    self.write_to_report(self.format, url, '', '', str(error))
                    self.error_list.append([url,error])
            except (NameError,mechanize.FormNotFoundError),error:
                self._warn('FIXME:',url,error)
                self.write_to_report(self.format, url, '', '', str(error))
                self.error_list.append([url,error])
            except (URLError,InvalidURL),error:
                    #if URLError occurs, log info about it to log file, but does not exit
                    self._warn("Is this URL:",url," valid?\n",error)
                    self.write_to_report(self.format, url, '', '', str(error))
                    self.error_list.append([url,error])
        #clear list:            
        self.test_list = []
                        
    def __check_all_subPages(self):
        link_list = []
        final_list = []
        
        self.main_url_host = self.url_host
        #for link in self._opener.links(url_regex="/*"):
        for link in self._opener.links():
           if link.url.startswith('http') or link.url.startswith('/'):
               link_list.append(link.url.lower()) 
               #.lower() since URLs are case.insensitive!
               #'/TDP/MACK-CA/EN-MC/TRAINING/PAGES/TRAINING.ASPX'
               #is the same as:
               #'/tdp/mack-ca/en-mc/training/pages/training.aspx'
        
        #make every URL unique: -> create final_list using list comprehension
        [final_list.append(link) for link in link_list if link not in final_list]
        #=====equivalent to the above:==============================================================
        # for link in link_list:
        #  if link not in final_list:
        #      final_list.append(link)
        #===================================================================
        pprint.pprint(final_list)
        self._info("1:",str(len(link_list)))
        self._info("2:",str(len(final_list)))
        
        for url in final_list:
            #get url_hostname (current self.url_host)
            if url.startswith('http'):  #exclude urls that start with '/'
                self._get_url_host(url)
            try:
                #with this url we stay in the same hostname area:
                if url.startswith('/') or self.url_host == self.main_url_host:
                    #response = self._opener.open_novisit(url) 
                    response = self._opener.open(url)
                    #check for the errors:
                    self._check_url_for_error(url)
                    if self.time_out:           #check_url returns self.time_out=True if time_out 
                        self._info('>>Request timed out - trying again [%s]'%url)
                        response = self._opener.open(url)
                        self._check_url_for_error(url)
                    url = response.geturl()
                    r_code = response.code
                    ip_addr = socket.gethostbyaddr(urlparse.urlparse(response.geturl()).netloc)
                    self._info("(hostname/aliases/IPlist):",ip_addr)
                    ip_addr = str(ip_addr[0])+" / "+str(ip_addr[2][0])
                    error = None
                    self.write_to_report(self.format, url, ip_addr, r_code, error)
                    
                else:
                    print '\n'
                    self._info('Skipping [%s] due to diff domain'%url)
                    self.skipped_list.append(url)

            except (URLError,InvalidURL,BrowserStateError,socket.error),error:  
                self.write_to_report(self.format, url, '', '', str(error))
                self.error_list.append([url,error])
                
                                
class Run_URL_Checks_Through_Proxy(Check_URLs):
    def __init__(self):
        Check_URLs.__init__(self)
    def check_urls(self):
        if self.run_proxy:
            self._info('Checking URLs through PROXY')
            self.write_to_report(self.format,"Host_Server:","PROXY","","")
            t0 = time.clock()
            self.hit_server_with_urls()    #there is switcher inside method (PROXY/NoProxy)
            overall_time = time.clock()-t0
            self.write_to_report(self.format,"","RUN_TIME: %.01f [s]"%(overall_time),"","")
            self.write_to_report(self.format,60*"*",20*"*",10*"*","") 
            self.save_report()      
        
class Run_URL_Checks(Check_URLs):
    '''
    content of the /etc:
    >>>>
    Server_hosts_1
    Server_hosts_2 
    Server_hosts_3
    Server_hosts_4
    hosts
    <<<<
    
    1.rename host_original -> host_backUp
    2.iteratively rename Server_hosts_X -> host_original
        3.run URL checks
        4.rename-back host_original -> Server_hosts_X
    5.When all servers checked, rename host_backUp -> host_original 
    '''
    def __init__(self):
        #list all the files from PATH_HOSTS (~/etc dir)
        self.all_files = [f for f in listdir(PATH_HOSTS) if isfile(join(PATH_HOSTS,f))]
        #get QA hosts file from PATH_HOSTS (~/etc dir)
        self.qa_host = [f for f in listdir(PATH_HOSTS) if isfile(join(PATH_HOSTS,f)) and f=='QA']
        self.end = False
        #create instance of the Check_URLs class
        Check_URLs.__init__(self)
        sys.stdout = loggers.Logger(detailed_log)
        
    def backUp_originalHost(self):
        #backup original host file
        #find host file
        if host_original in self.all_files:
            try:
                #create backUp of the original host file (rename)
                os.rename(os.path.join(PATH_HOSTS,host_original), os.path.join(PATH_HOSTS,host_backUp))
                self._info('BackUp of the original HOST file: host-> %s' % host_backUp)
                
                return True
            except WindowsError,e:
                self._info('%s already exists!, \n%s' %(os.path.join(PATH_HOSTS,host_backUp),e))
                return False
        else: 
            self._warn('Original host file not found in "%s"' % (PATH_HOSTS))
            return False
             
    def setServerHostFile_and_RunUrlChecks(self):
        #get lists with urls:
        self.inet_list_bkp, self.xnet_list_bkp, self.qa_inet_list_bkp, self.qa_xnet_list_bkp = self.get_listOf_URLs()
        #create request (browser instance -> self._opener obj:
        Get_Browser.__init__(self)
        
        self._info("setServerHostFile_and_RunUrlChecks:self.all_files:",self.checklist)
        t0 = time.clock()
        if self.production_run:
            #Verify Production URLs:
            for host_server in self.checklist:
                self.inet_list = self.inet_list_bkp[:]
                self.xnet_list = self.xnet_list_bkp[:]

                self._info('using host_server:',host_server)
                self.write_to_report(self.format,"Host_Server:",host_server,"","")
                try:
                    #rename Server-Oriented host to Windows-Oriented host (SEGOTN2525 to host)
                    os.rename(os.path.join(PATH_HOSTS,host_server), os.path.join(PATH_HOSTS,host_original))
                    #EXECUTE URL CHECKS
                    t1 = time.clock()
                    self.hit_production_servers_with_urls()
                    after_time = time.clock()-t1
                    self.write_to_report(self.format,"","RUN_TIME: %.01f [s]"%(after_time),"","")
                    self.write_to_report(self.format,60*"*",20*"*",10*"*","") 
                except KeyboardInterrupt, ValueError:
                    #ValueError occurs when there are too many values to write to XLS (>4096)
                    print '\n'
                    self._warn('Stopped by user! Reverting to the original hosts...')
                    self.write_to_report(self.format,"","RUN_TIME: %.01f [s]"%(time.clock()-t1),"","")
                    self.write_to_report(self.format, 'Stopped by user!', '', '', 'Keyboard Interrupt')
                    self.save_report()
                    #revert Windows-Oriented host to Server-Oriented host (host to SEGOTN2525)
                    os.rename(os.path.join(PATH_HOSTS,host_original), os.path.join(PATH_HOSTS,host_server))
                    self.end = True
                    self.set_OriginalHost()
                    sys.exit()
                
                #when checking is done, revert Windows-Oriented host to Server-Oriented host (host to SEGOTN2525)
                os.rename(os.path.join(PATH_HOSTS,host_original), os.path.join(PATH_HOSTS,host_server))
                self._info('-->next....')
            
        #Verify QA URLs:
        if self.qa_run and self.qa_host:
            self.qa_inet_list = self.qa_inet_list_bkp[:]
            self.qa_xnet_list = self.qa_xnet_list_bkp[:]
            qa_host=self.qa_host[0]
            self._info('using host_server:',qa_host)
            self.write_to_report(self.format,"Host_Server:",qa_host,"","")
            try:
                #rename Server-Oriented host to Windows-Oriented host (SEGOTN2525 to host)
                os.rename(os.path.join(PATH_HOSTS,qa_host), os.path.join(PATH_HOSTS,host_original))
                #EXECUTE URL CHECKS
                t1 = time.clock()
                self.hit_qa_servers_with_urls()
                after_time = time.clock()-t1
                self.write_to_report(self.format,"","RUN_TIME: %.01f [s]"%(after_time),"","")
                self.write_to_report(self.format,60*"*",20*"*",10*"*","") 
            except KeyboardInterrupt, ValueError:
                #ValueError occurs when there are too many values to write to XLS (>4096)
                print '\n'
                self._warn('Stopped by user! Reverting to the original hosts...')
                self.write_to_report(self.format,"","RUN_TIME: %.01f [s]"%(time.clock()-t1),"","")
                self.write_to_report(self.format, 'Stopped by user!', '', '', 'Keyboard Interrupt')
                self.save_report()
                #revert Windows-Oriented host to Server-Oriented host (host to SEGOTN2525)
                os.rename(os.path.join(PATH_HOSTS,host_original), os.path.join(PATH_HOSTS,qa_host))
                self.end = True
                self.set_OriginalHost()
                sys.exit()
            
            #when checking is done, revert Windows-Oriented host to Server-Oriented host (host to SEGOTN2525)
            os.rename(os.path.join(PATH_HOSTS,host_original), os.path.join(PATH_HOSTS,qa_host))
            
        #close browser instance:
        self._opener.close() 
        
        #log overall time:
        overall_time = time.clock()-t0
        if overall_time>60:
            self.write_to_report(self.format,"","RUN_TIME_OVERALL: %d[m]%d[s]"%(overall_time/60,overall_time%60),"","")
        else:
            self.write_to_report(self.format,"","RUN_TIME_OVERALL: %.01f [s]"%(overall_time),"","")
        #when all the host_server's file used, revert to the original host file       
        self.end = True
        self.save_report()
        
    def set_OriginalHost(self):
        """if self.end is True, revert host to the original host file
        """
        if self.end:
            #get list of all the files in PATH_HOSTS
            files = [f for f in listdir(PATH_HOSTS) if isfile(join(PATH_HOSTS,f))]
            if host_backUp in files:
                self._info("renaming host_backUp to original hosts file...")
                os.rename(os.path.join(PATH_HOSTS, host_backUp), os.path.join(PATH_HOSTS,host_original))
                self._info('Done')
                #sys.exit()
        else:
            self._warn('Problem with reverting to original host file!')

    def send_mail(self,**kwargs):
        """available args:
        [to,cc,bcc,body,subject,attachment]
        pass arguments as below:
        (Cc='this_is_cc',Body='this_is_body', to='test@test.test')
        """
        MailItem = 0x0
        outlook = win32com.client.Dispatch("Outlook.Application")
        newMail = outlook.CreateItem(MailItem)
        
        for key in kwargs:
            if re.search(r'[Tt]o',key):
                newMail.To = kwargs[key]
            elif re.search(r'[Cc]c',key):
                newMail.CC = kwargs[key]
            elif re.search(r'[Bb]cc',key):
                newMail.Bcc = kwargs[key]
            elif re.search(r'[Ss]ubject', key):
                newMail.Subject = kwargs[key]
            elif re.search(r'[Bb]ody',key):
                newMail.Body = kwargs[key]
            elif re.search(r'[Aa]ttachments',key):
                newMail.Attachments.Add(kwargs[key])
            else:
                print '>>'+strftime("%H:%M:%S")+' Send_mail: incorrect key! [%s]' % key
        #newMail.display()
        newMail.Send()
        
        print '>>'+strftime("%H:%M:%S")+'<< Email with the results sent to the recipients!'
     
def main():
    if run_URL_checks_through_PROXY:
        obj = Run_URL_Checks_Through_Proxy()
        obj.hit_server_with_urls()
    else:
        obj = Run_URL_Checks()
        if obj.backUp_originalHost():
            obj.setServerHostFile_and_RunUrlChecks()
        obj.set_OriginalHost()
        """
        sendmail with resutls to the recipients
        """
        if obj.to and not obj.cc:
            obj.send_mail(To=obj.to, Subject='URL_Checker has finished!'\
                  ,Body='Log attached\n\nDetailed Log: [%s]'%detailed_log, Attachments=report_file)
        if obj.to and obj.cc:
            obj.send_mail(To=obj.to, Cc=obj.cc, Subject='URL_Checker has finished!'\
                  ,Body='Log attached', Attachments=report_file)
    sys.exit()
    
if __name__ == '__main__':
    main()
