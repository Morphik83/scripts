import mechanize
import pprint
import re
import sys
import os
import urlparse
import loggers
import time
from _root import *
from config_file import * 
from urllib2 import URLError
from httplib import InvalidURL


class Get_Browser(RootClass):
    '''
    creates browser's instance; feeds CheckURLs
    '''     
    def __init__(self):
        self._opener = self._browser()

    def _browser(self):
        browser = mechanize.Browser()
        browser.set_debug_http(True)
        browser.set_handle_robots(False)
        browser.set_debug_redirects(True)
        browser.set_debug_responses(True)
        browser.addheaders=[headers]
        return browser
    
    def login_to_xnet(self, username, passwd):
        self._opener.select_form(nr=0)
        self._opener["ctl00$BodyContent$login$UserName"]=username
        self._opener["ctl00$BodyContent$login$Password"]=passwd
        self._opener.submit(name='ctl00$BodyContent$login$LoginButton')


class Crawler(Get_Browser):
    def __init__(self, start_url, enable_proxy):
        self.links_to_follow = []
        self.visited_urls = []
        self.error_list = []
        self.enable_proxy = enable_proxy
        self.start_url = start_url
        self.host_url = self._get_url_host(self.start_url)
        Get_Browser.__init__(self)
        #redirect sys.stdout (all print statements) to Logger obj (->sys.stdout & crawler_log file
        sys.stdout = loggers.Logger(self.add_hostname_to_crawler_log())
    
    def add_hostname_to_crawler_log(self):    
        '''inserts start_url hostname to the crawler log file
        before: D:\workspace\Git\scripts\web_crawler\logs\13-01-31_13_22_45_CRAWLER.log
        after:  D:\workspace\Git\scripts\web_crawler\logs\[volvo.com]13-01-31_13_22_45_CRAWLER.log
        '''
        pttrn = re.compile(r'(.*\\)(.*$)')
        result = re.search(pttrn, crawler_log)
        if result:
            return result.group(1)+'['+self.net_loc+']'+result.group(2)
        else:
            self._warn('add_hostname_to_crawler_log: Cannot add hostname to the crawler_log!')
        
    def _get_url_host(self,url):
        self._info('Validating url ...')
        parsed = urlparse.urlparse(url)
        if parsed.scheme and parsed.netloc and re.match(r'http[s]?',parsed.scheme):
            self.net_loc = parsed.netloc
            self.host_url = parsed.scheme + '://' + parsed.netloc
            return self.host_url
        else:
            self._warn('_get_url_host: Cannot find hostname in given url! [',url,']')
            self._warn('Closing the script')
            sys.exit()
    
    def check_url_for_error(self, url):
        response = self._opener.response()
        the_page = response.read()
        self._info("-->checking [%s] for errors... [page length: %d] " %(url,len(the_page)))
        search = re.search(r'(\w+\sis not available)|(is not available)|(Technical information is available in the error log)', the_page)
        if search:
            self._warn('CHECK THIS URL:\n[%s]\n[%s]!\n' %(url, search.group(1)))
            self.error_list.append([url,search.group(1)])
        else:
            self._info('no errors noticed\n')
                    
    def run_crawler(self):
        def _update_visited_urls(self, url):
            self.visited_urls.append(url)
        def _update_links_to_follow(self, url):
            self.links_to_follow.append(url)
        def _delete_url_from_links_to_follow(self, url):
            self.links_to_follow.pop(self.links_to_follow.index(url))
        try:    
            self._info('Starting CWP_Web_Crawler ...\n\n')
            time.sleep(2)
            if self.enable_proxy:
                try:
                    print 'IMPORT getProxy'
                    import get_PROXY
                except ImportError,e:
                    print e
                proxies = get_PROXY.get_proxy_from_pac(pacfile, self.start_url)
                self._opener.set_proxies(proxies)
        
            #start timer
            t0 = time.clock()
            #open start_url
            try:
                self._opener.open(self.start_url)
            except URLError,e:
                self._warn("is this URL: [",str(self.start_url),"] valid?\n",str(e))
                self.error_list.append([self.start_url,str(e)])
                sys.exit()
            #login to xnet
            try:
                self.login_to_xnet(username, passwd)
            #except (mechanize.ControlNotFoundError,mechanize.FormNotFoundError),e:
            except (mechanize.ControlNotFoundError,mechanize.FormNotFoundError),e:
                self._info('ALREADY LOGGED OR INET PAGE')
            #get all valid links
            finally:
                #check start_url for errors:
                self.check_url_for_error(self.start_url)
                self._info('>>scraping...')
                for link in self._opener.links():
                    if link.url.startswith(self.host_url) or link.url.startswith('/') :
                        if link.url not in self.links_to_follow:
                            if link.url not in self.visited_urls:
                                self._info('-->links_to_follow.append: %s ' % link.url)
                                _update_links_to_follow(self, link.url)
                            else:
                                self._info('-->skipping: %s ' % link.url)
                                
                _update_visited_urls(self, self.start_url)
                self._info('-->link_to_follow.length: [%d]' % len(self.links_to_follow))
                print '\n'
                self._info('------------------->> NEXT <<-------------------')
                
            while self.links_to_follow:
                try:
                    url = self.links_to_follow[0]
                    self._info('>>opening: [%s] \n' % url)
                    self._opener.open(url)
                    #check for error:
                    self.check_url_for_error(url)
                    self._info('>>scraping...')
                    for link in self._opener.links():
                        if link.url.startswith(self.host_url) or link.url.startswith('/') :
                            if link.url not in self.links_to_follow:
                                if link.url not in self.visited_urls:
                                    self._info('-->links_to_follow.append: %s ' % link.url)
                                    _update_links_to_follow(self, link.url)
                                else:
                                    self._warn('-->skipping: %s ' % link.url)
                
                except mechanize.BrowserStateError,e:
                    if str(e)== 'not viewing HTML':
                        self._info('URL points to document! [',url,']')
                    else:
                        self._warn("is this URL: [",str(url),"] valid?\n",str(e))
                        self.error_list.append([url,str(e)])
                
                except (URLError,InvalidURL,IndexError),e:
                    self._warn("is this URL:",str(url)," valid?\n",str(e))
                    self.error_list.append([url,str(e)])
    
                finally:
                    #before getting next url from list, update:
                    _update_visited_urls(self, url)
                    self._info('-->link_to_follow.delete: %s ' % url)
                    _delete_url_from_links_to_follow(self, url)
                    
                    self._info('-->link_to_follow.length: [%d]' % len(self.links_to_follow))
                    self._info('-->visited_links.length: [%d] ' % len(self.visited_urls))
                    self._info('-->error_list.length: [%d] '%len(self.error_list))
                    self._warn('error_list:')
                    pprint.pprint(self.error_list)
                    print '\n'
                    self._info('------------------->> NEXT <<-------------------') 
                          
            overall_time = time.clock()-t0
            print '\n'
            self._info('>>>>>>> SCRIPT IS DONE <<<<<<<<<')
            if overall_time>60:
                self._info('RUN_TIME_OVERALL: %d[m]%d[s]' %(overall_time/60,overall_time%60))
            else:
                self._info('RUN_TIME_OVERALL: %.01f [s]' %overall_time)
            self._info('visited_links.length: [%d] ' % len(self.visited_urls))
            self._info('error_list.length: [%d] '%len(self.error_list))
            self._warn('error_list:')
            pprint.pprint(self.error_list)
        
        except KeyboardInterrupt:
            print '\n'
            self._warn('Stopped by user!')
            sys.exit()

class Menu(Crawler, RootClass):
    '''simple menu with  basic selections
    '''
    def __init__(self):
        self.welcome_page()
        start_url, enable_proxy = self.get_info()
        Crawler.__init__(self, start_url, enable_proxy)
        self.run_crawler()
        
    def welcome_page(self):
        self._info('>> Web_Crawler << author: Maciej Balazy >>')
        time.sleep(2)
        print (INTRO)
        
    def get_info(self):
        start_url = raw_input('> Provide start_url [must start with http://] : ')
        proxy = raw_input('> Enable PROXY ?[y/n]: ')
        print 
        if proxy == 'y':
            enable_proxy = True
        else:
            enable_proxy = False
        return start_url, enable_proxy 
        
def main():
    #to run from Run_Crawler.bat where you can provide start_url
    try:
        obj = Menu()
    finally:
        sys.stdout = sys.__stdout__     #revert sys.stdout to normal

if __name__ == '__main__':
    main()
    
