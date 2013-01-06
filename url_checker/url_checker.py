import urllib2
import urlparse
import socket 
import os
import sys
import re
import pprint
import shutil
import time
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
        self.host_list = []
        self.checklist=[]
        self.menu()
        
    def menu(self):
        def _menu_check_subPages(self):
            """set True/False whether you want to check all the subpages on the given page
            set TRUE  if all the links from given page should be checked as well 
            (eg. http://volovit.com -> any link that exists on that page will be checked) 
            set FALSE if only pages from URLS.input file should be checked
            """
            check = raw_input('Do you want to verify sub_pages? [y/n]: ')
            if re.search(r'\b[yY]\b|\byes\b|\bYES\b',check):
                self.check_all_subPages = True
                self._info('check_all_subPages: TRUE')
                return self.check_all_subPages
            elif re.search(r'\b[nN]\b|\bno\b|\bNO\b',check):
                self.check_all_subPages = False
                self._info('check_all_subPages: FALSE')
                return self.check_all_subPages
            else:
                self._warn('Not valid answer! Valid: [y/n]')
                _menu_check_subPages(self)
                
        def _menu_add_servers(self):
            def _for_host_server(self):
                for host_server in self.host_list:
                    msg = ''.join(['Add [',host_server,'] to checklist? [y/n]: '])
                    yes_no = raw_input(msg)
                    if re.search(r'\b[yY]\b|\byes\b|\bYES\b',yes_no):
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
                    elif re.search(r'\b[nN]\b|\bno\b|\bNO\b',yes_no):
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
                        self._warn('Not valid answer! Valid: [y/n]\n')
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
            self.host_list = []
            for host_server in self.all_files:
                if re.search(server_hosts_pattern, host_server):
                    self.host_list.append(host_server)
                    
            #self._info('Available server-host files: ',self.host_list)
            self._info('Select servers:')
            self._info('Available server-host files: ',self.host_list,'\n')
            _for_host_server(self)
            
            if len(self.checklist)==0:
                self._warn('Current checklist is empty!\nNo servers selected!\nStart again...')
                sys.exit()
            else:
                self._info('>>>>>>CURRENT  CONFIGURATION:')
                self._info('URLs from %s will be verified on the following servers: ' % file_with_urls)
                self._info(self.checklist)
                if self.check_all_subPages:
                    self._info('Check subpages: True')
                else:    
                    self._info('Check subpages: False')
                self._info('Report file will be saved here: ',report_file)
                go = raw_input("Run ? [y/n] ")
                if re.search(r'\b[yY]\b|\byes\b|\bYES\b',go):
                    
                    pass
                else:
                    self._info('Exiting...\nStart program again')
                    sys.exit()
                    
        #sets check_all_subPages=True/False
        _menu_check_subPages(self)
        
        #select server_host files
        _menu_add_servers(self)
          
        #run the script on the selected only servers

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
        self.error_list = []
        self.lists_with_urls = []
        self.format = self._getFileExt()
        self.run_proxy = run_URL_checks_through_PROXY
        #creates Report Object (dependently on given file format)
        Report.__init__(self, self.format, self.report)
        #start simple menu
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
                       except AttributeError,e:                 #if no [X]|[I] are found, then verify urls 
                           self._warn('ERROR: %s verify prefix!  e:%s' % (line,e))
                           if line not in self.error_list:  #to avoid appending the same info for each server - log only once
                               self.error_list.append(line)
               
        return self.inet_list, self.xnet_list, self.error_list        #when parsing is done, return 3 lists
    
    def hit_server_with_urls(self):
        #get lists with urls:
        self.get_listOf_URLs()
        #create request (browser instance -> self._opener obj:
        Get_Browser.__init__(self)
        
        #self.test_list defined, since __check_url is used for both inet & xnet
        if self.inet_list:
            self.test_list = self.inet_list      
            self.__check_url(self.check_all_subPages, xnet_login=False)
        if self.xnet_list:
            self.test_list = self.xnet_list
            self.__check_url(self.check_all_subPages, xnet_login=True)
        
        #clear lists content:
        self.inet_list = []
        self.xnet_list = []
        #close browser instance:
        self._opener.close()   
        self._warn('Check these URLs: ',self.error_list)    
            
    def __check_url(self, check_all_subPages, xnet_login):
        for url in self.test_list:
            try:    
                if self.run_proxy:
                    self._info('GETTING PROXY...')
                    proxies = get_PROXY.get_proxy_from_pac(pacfile, url)
                    self._opener.set_proxies(proxies)
                
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
                
                #get status:
                r_code = response.code
                #ip_addr = socket.gethostbyname(urlparse.urlparse(response.geturl()).netloc)
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
                    
            except mechanize.ControlNotFoundError,e:
                """
                ControlNotFoundError occurs when no Login/Pass forms are located on the page -> it might be that 
                the user is already logged in, so that is why the return code (200) is checked. 
                """
                try:
                    assert response.code == 200
                    self._info('Return Code is 200')
                    ip_addr = socket.gethostbyaddr(urlparse.urlparse(response.geturl()).netloc)
                    ip_addr = str(ip_addr[0])+" / "+str(ip_addr[2][0])
                    r_code = response.code
                    error = None
                    self.write_to_report(self.format, response.geturl(), ip_addr, r_code, error)
                    if check_all_subPages:
                        self.__check_all_subPages()
                except AssertionError,e:
                    self._warn('Return code is not 200! It is: ',e)
                    error = e
                    self.write_to_report(self.format, url, '', '', error)
                    
            except (NameError,mechanize.FormNotFoundError),e:
                self._warn('FIXME:',url,e)
                error = e
                self.write_to_report(self.format, url, '', '', error)
            except (URLError,InvalidURL),e:
                    #if URLError occurs, log info about it to log file, but does not exit
                    self._warn("Is this URL:",url," valid?\n",e)
                    error = e
                    self.write_to_report(self.format, url, '', '', error)
                    self.error_list.append([url,error])
        #clear list:            
        self.test_list = []
        
        #=======================================================================
        #--> this is how we can check urls with bare urllib2
        # for url in self.inet_list:
        #    request = urllib2.Request(url, None, self.headers)
        #    try:
        #        response = self.inet_opener.open(request)
        #        #ip_addr = socket.gethostbyname(urlparse.urlparse(response.geturl()).netloc)
        #        ip_addr = socket.gethostbyaddr(urlparse.urlparse(r.geturl()).netloc)
        #        r_code = response.getcode()
        #        #print '\nURL:',url
        #        #print '\nCode:',r_code
        #        #print '\nIP:',ip_addr
        #        error =  None
        #        self.write_to_report(self.format, url, ip_addr, r_code, error)
        #    except (URLError,InvalidURL),e:
        #        #if URLError occurs, log info about it to log file, but does not exit
        #        print "Is this URL:",url," valid?\n",e
        #        error = e
        #        self.write_to_report(self.format, url, '', '', error)
        # self.inet_list = []      
        #=======================================================================
                
    def __check_all_subPages(self):
        link_list = []
        final_list = []
        for link in self._opener.links(url_regex="/*"):
           if link.url.startswith('http') or link.url.startswith('/') :
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
            try:
                response = self._opener.open_novisit(url) 
                #r = self.xnet_opener.open(url)
                url = response.geturl()
                r_code = response.code
                ip_addr = socket.gethostbyaddr(urlparse.urlparse(response.geturl()).netloc)
                self._info("(hostname/aliases/IPlist):",ip_addr)
                ip_addr = str(ip_addr[0])+" / "+str(ip_addr[2][0])
                error = None
                self.write_to_report(self.format, url, ip_addr, r_code, error)
              
            except (URLError,InvalidURL),e:  
                #sometimes links on the page redirects to some other hosts - we have one browser instance, that is 
                #following every link on the page (send Requests are created 'on the fly', so if page redirects
                #to other host, then HEADER in our browser's request is updated to the new host name.
                #Due to that, next links are send with improper(changed) HOSTNAME -> which results in 'HTTP 404 Page Not Found'
                #FIX: when '404' occurs, we are going back 2 pages (it may be different on diff sites...), to the page
                #when HOSTNAME was correct, and then we try to re-open the failing URL
                #I am aware, this is VERY error prone (IDEA: maybe counter in the loop - back n=1 ->check ->FAIL back n=2->
                #check ->FAIL back n=3... Up to predefined eg.n=5)
                #Other FIX is to use b.open_novisit(url) instead of b.open(url). In this case, browser state is unchanged
                #but it somehow closes the door for scraping deeper (eg.cannot get links from such page - so I cannot 
                #check them)
                self.write_to_report(self.format, url, '', '', str(e))
                #=========================================================
                # try:
                #    self.write_to_report(self.format, url, '', '', str(e))
                #    self.xnet_opener.back(n=2)
                #    r = self.xnet_opener.open(url)
                #    self.write_to_report(self.format, '', '', '', 'Probably Hostname was changed! BACK 2 pages...')
                #    ip_addr = socket.gethostbyaddr(urlparse.urlparse(r.geturl()).netloc)
                #    ip_addr = str(ip_addr[0])+"/"+str(ip_addr[2][0])
                #    self.write_to_report(self.format, r.geturl(), ip_addr, r.code, None)
                # except (URLError,InvalidURL),e:
                #    self.write_to_report(self.format, url, '', '', str(e))
                #=========================================================
            except socket.error,e:
               self.write_to_report(self.format, url, '', '', str(e))
                              
                    #=============================================================
                    #--> this does not occur when b.open_novisit(url) is used!
                    # except mechanize._mechanize.BrowserStateError,e:
                    #    #this error occurs, when 'Error 118 (net::ERR_CONNECTION_TIMED_OUT): The operation timed out.'
                    #    #Page is not available. Eg. Open Inet page (eg.www.volvobuses.com), get all the links from that page
                    #    #among other, there is XNET link (https://vbos.volvo.com/)
                    #=============================================================
                    
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
                self._info('BackUp of the original HOST file: host-> %s' % host_backUp)
                return True
            except WindowsError,e:
                self._info('%s already exists!, \n%s' %(os.path.join(PATH_HOSTS,host_backUp),e))
                return False
        else: 
            self._warn('Original host file not found in "%s"' % (PATH_HOSTS))
            return False
             
    def setServerHostFile_and_RunUrlChecks(self):
        #search for Server-Oriented host files:
        #server_hosts_pattern defined in config_file.py
        self.all_files = self.checklist
        self._info("setServerHostFile_and_RunUrlChecks:self.all_files:",self.all_files)
        for host_Server in self.all_files:
            if re.search(server_hosts_pattern, host_Server):
                self._info('using host_Server:',host_Server)
                self.write_to_report(self.format,"Host_Server:",host_Server,"","")
                #rename Server-Oriented host to Windows-Oriented host (SEGOTN2525 to host)
                os.rename(os.path.join(PATH_HOSTS,host_Server), os.path.join(PATH_HOSTS,host_original))
                #EXECUTE URL CHECKS
                t0 = time.clock()
                self.hit_server_with_urls()
                overall_time = time.clock()-t0
                self.write_to_report(self.format,"","RUN_TIME: %.01f [s]"%(overall_time),"","")
                self.write_to_report(self.format,60*"*",20*"*",10*"*","") 
                
                #when checking is done, revert Windows-Oriented host to Server-Oriented host (host to SEGOTN2525)
                os.rename(os.path.join(PATH_HOSTS,host_original), os.path.join(PATH_HOSTS,host_Server))
                self._info('-->next....')
        #when all the host_Server's file used, revert to the original host file       
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
                sys.exit()
        else:
            self._warn('Problem with reverting to original host file!')

def main():
    #check = Check_URLs()
    #check.hit_server_with_urls()
    if run_URL_checks_through_PROXY:
        obj = Run_URL_Checks_Through_Proxy
        obj.hit_server_with_urls()
    else:
        obj = Run_URL_Checks_OnServers()
        
        if obj.backUp_originalHost():
            obj.setServerHostFile_and_RunUrlChecks()
        obj.set_OriginalHost()    

if __name__ == '__main__':
    main()
