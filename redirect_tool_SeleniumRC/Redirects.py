from SeleniumLibrary import SeleniumLibrary
from _root import RootClass
import time
import os
import re
from win32com.client import Dispatch

TIMEOUT = 30000
SHELL = Dispatch("Shell.Application")

_LOCAL_TIME = time.asctime(time.localtime(time.time()))
LOCAL_TIME = re.sub(r'[: ]','_',_LOCAL_TIME)

LOG_DIR = 'D:\\tmp\\logs'
REDIRECT_INPUT_FILE = 'D:\\tmp\\Redirects.input'
REDIRECT_REPORT_FILE = open (os.path.join(LOG_DIR,'RedirectsReport.html'), "a+")
REDIRECT_LOG_FILE = open (os.path.join(LOG_DIR,'redirects.log'), "a+")

class Redirects(RootClass):
    
    def __init__(self):
        self.selLib = SeleniumLibrary()
        
    def shut_Down_All_Browsers(self):
        self.selLib.close_all_browsers()
        self._info("All browsers closed")
        
    def start_selenium_server_XX(self, profile=None):
        self.selLib.start_selenium_server()
        
    def start_browser(self, url,browser=None):
        if browser == None:
            browser = 'ie'
        self.selLib.set_selenium_timeout(TIMEOUT)
        self.selLib.open_browser(url, browser)
        
    def get_ie(self, shell):
        """
        get IE browser as object
        """
        for win in shell.Windows():
            try:
                if win.Name == "Windows Internet Explorer":
                    return win
            except AttributeError:
                #this is to handle some <unknown> COMObject
                pass
        return None
    
    
    def createReport(self):
        
        body = "<html> <body>" \
               "<h1>Redirects Tests Results</h1> <p>%s</p>""</body> </html>" %(LOCAL_TIME)
        REDIRECT_REPORT_FILE.write(body)
        REDIRECT_LOG_FILE.write("Redirects Tests Results: %s \n" %LOCAL_TIME)
        
    def get_url(self, url, address):
        ie = self.get_ie(SHELL)
        if ie:
            if str(ie.LocationURL) == address:
                self._info("PASS: address %s is redirected to %s" % (url, address))
                REDIRECT_LOG_FILE.write("PASS: address %s is redirected to %s\n" % (url, address))
                REDIRECT_REPORT_FILE.write("<ul><li><font size='3'color='green'><b>PASSED</b></font>\tAddress: \
                <b><a href=%s>%s</a></b> \n    \tredirects to: <b><a href=%s>%s</a></b>\n\n</li></ul>" % (url,url, address,address))
            else:
                self._info('FAIL: address %s is not redirected to %s' % (url, address))
                REDIRECT_LOG_FILE.write('FAIL: address %s is not redirected to %s\n' % (url, address))
                REDIRECT_REPORT_FILE.write("<ul><li><font size='3'color='red'><b>FAILED</b></font>\tAddress: \
                <b><a href=%s>%s</a></b> \n    \tis not redirected to: <b><a href=%s>%s</a></b>\n\n</li></ul>" % (url,url, address,address))
                REDIRECT_REPORT_FILE.write("<ul><li><font size='3'color='red'><b>FAILED</b></font>\tAddress: \
                <b><a href=%s>%s</a></b> \n    \tis redirected to: <b><a href=%s>%s</a></b>\n\n</li></ul>" % (url,url, ie.LocationURL,ie.LocationURL))
            #REDIRECT_REPORT_FILE.close()
        else:
            print "no ie window"
      
    def verify_Redirects(self, input_file):
        """
        redirect_input_file:
        
        url_1 url_2
        #url_1 url_2 
        (...)
        url_1 ->origin
        url_2 -> target 
        if #: skip the line
        """
        redirects_input_file = open(input_file, 'r+')
        searchPattern = re.compile(r'(^[^\/#].*?)\s(.*$)')
        # in reg_exp ? is used for non-greedy search pattern - without ?, first match will cover whole line (up to $) due to .*

        for line in redirects_input_file:
            search = re.search(searchPattern, line)
            if search != None:
                #if url_1 has no 'http://' prefix, then add one:
                if search.group(1).find('://') == -1:
                    url_1 = 'http://%s' % (search.group(1),)
                else:
                    url_1 = search.group(1)
                #the same here, with url_2 (target)
                if search.group(2).find('://') == -1:
                    url_2 = 'http://%s' % (search.group(2),)
                else:
                    url_2 = search.group(2)   
                
                #finally, start browser:
                self.start_browser(url_1, browser='ie')
                #verify if addresses are redirected as expected:
                self.get_url(url_1, url_2)
                
                #afterall, close/shutdown browser:
                self.shut_Down_All_Browsers()
                self.selLib.close_browser()
              
            else:
                self._info("Skipping...")
                

if __name__ == '__main__':
    test = Redirects()
    test.createReport()
    test.verify_Redirects(REDIRECT_INPUT_FILE)
        
    #===========================================================================
    # import urllib2
    # request = urllib2.Request('http://www.volvoce.com/wheeledexcavators/eu/fr/')
    # print urllib2.urlopen(request).info()
    #===========================================================================
    #print reesponse.info()
    
    #============================================================================
    #import twill
    #go(<here goes any http:// address>)
    #===========================================================================
    # test_str = "#http://www.volvogroup.com http://www.volvogroup.com/group/global/en-gb/Pages/group_home.aspx"
    # searchPattern = re.compile(r'(^.*)\s(.*$)')
    # search_result = re.search(searchPattern, test_str)
    # if search_result != None:
    #    print search_result.group(0)
    #    print search_result.group(1)
    #    print search_result.group(2)
    # else:
    #    print "skipping..."
    # 
    #===========================================================================
    

    
    