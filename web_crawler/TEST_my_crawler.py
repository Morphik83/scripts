import mechanize
from urllib2 import URLError
from httplib import InvalidURL
import pprint
import re
import sys
import os
import _root
import urlparse
from _root import RootClass
import config_file

from config_file import *
"""
start_url = ''
urls_to_follow = []
visited_urls = []

open start_url
    get_urls -> urls_to_follow.append
    visisted_urls.append(start_url) 

for url in urls_to_follow:
    open url
    get_urls -> if url not in urls_to_follow and not in visited_urls:
                    urls_to_follow.append
    visited_urls.append(url)
    urls_to_follow(urls_to_follow.index(url))

when is it done? -> we open urls one by one from urls_to_follow, and after some time
all the links parsed, will be already in either urls_to_follow list or visisted_urls list, 
so such links won't be appended to either list. 
In that way, urls_to_follow should start to shrink eventually
"""


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

    

class Logs(RootClass):
    '''
    creates log objects
    '''
    def __init__(self, crawler_log, error_log):
        self.crawler_log = open(crawler_log, 'a+')
        self.error_log = open(error_log, 'a+')

class Crawler(Get_Browser, Logs):
    def __init__(self):
        self.links_to_follow = []
        self.visited_urls = []
        self.error_list = []
        self.start_url = start_url
        self.host_url = self._get_url_host(self.start_url)
        Get_Browser.__init__(self)
        Logs.__init__(self, crawler_log, error_log)
    
    def _get_url_host(self,url):
        parsed = urlparse.urlparse(url)
        if parsed.scheme and parsed.netloc:
            url_host = parsed.scheme + '://' + parsed.netloc
            return url_host
        else:
            self._warn('_get_url_host: Cannot find hostname in given url! [',url,']')
    
    def check_url_for_error(self, url, f, er):
        print type(f)
        print f
        print type(er)
        print er
        
        er.write('FGHJKLJHVGCVBNM')
        print '\n'
        response = self._opener.response()
        self._info("Parsing opened page...")
        f.write("Parsing opened page...\n")
        the_page = response.read()
        self._info("--->Checking [%s] for errors... len(the_page): [%d]\n" %(url,len(the_page)))
        f.write("Checking [%s] for errors... \n" %url)
        search = re.search(r'(\w+\sis not available)|(is not available)|(Technical information is available in the error log)', the_page)
        er.write(url)
        if search:
            print 'CHECK THIS URL:\n[%s]\n[%s]!\n' %(url, search.group(1))
            er.write('CHECK THIS URL:\n[%s]\n[%s]!\n' %(url, search.group(1)))
            self.error_list.append(url)
        else:
            print 'No errors noticed\n'
            f.write('No errors noticed\n')
            
    def run_crawler(self):
        
        def _update_visited_urls(self, url):
            self.visited_urls.append(url)
        def _update_links_to_follow(self, url):
            self.links_to_follow.append(url)
        def _delete_url_from_links_to_follow(self, url):
            self.links_to_follow.pop(self.links_to_follow.index(url))
            
        
        with self.crawler_log:
            with self.error_log:
                #open start_url
                self.crawler_log.write('##OPEN %s \n' % self.start_url)
                self._opener.open(start_url)
                #login to xnet
                try:
                    self.login_to_xnet(username, passwd)
                except mechanize.ControlNotFoundError,e:
                    print 'ALREADY LOGGED'
                #get all valid links
                finally:
                    #check start_url for errors:
                    self.check_url_for_error(start_url, self.crawler_log, self.error_log)
                    for link in self._opener.links():
                        if link.url.startswith(self.host_url) or link.url.startswith('/') :
                            if link.url not in self.links_to_follow:
                                if link.url not in self.visited_urls:
                                    self.crawler_log.write('--->links_to_follow.append: %s \n' % link.url)
                                    _update_links_to_follow(self, link.url)
                                else:
                                    self.crawler_log.write('--->skipping: %s \n' % link.url)
                                    
                    _update_visited_urls(self, self.start_url)
                    self.crawler_log.write('START: len of links_to_follow: [%d]\n' % len(self.links_to_follow))
                    pprint.pprint(self.links_to_follow)
                
                while self.links_to_follow:
                    try:
                        url = self.links_to_follow[0]
                        self.crawler_log.write('####NEXT URL: opening [%s] \n' % url)
                        self._opener.open(url)
                        #check for error:
                        self.check_url_for_error(url, self.crawler_log, self.error_log)
                        for link in self._opener.links():
                            if link.url.startswith(self.host_url) or link.url.startswith('/') :
                                if link.url not in self.links_to_follow:
                                    if link.url not in self.visited_urls:
                                        self.crawler_log.write('--->links_to_follow.append: %s \n' % link.url)
                                        _update_links_to_follow(self, link.url)
                                    else:
                                        self.crawler_log.write('--->skipping: %s \n' % link.url)
                        #before getting next url from list, update:
                        self.crawler_log.write('**VISITED_URLS: %s \n' % url)
                        _update_visited_urls(self, url)
                        self.crawler_log.write('Before_POP: len of links_to_follow: [%d]\n' % len(self.links_to_follow))
                        self.crawler_log.write('Pop: %s \n' % url)
                        _delete_url_from_links_to_follow(self, url)
                        self.crawler_log.write('After_POP: len of links_to_follow: [%d]\n' % len(self.links_to_follow))
                        self.crawler_log.write('--------------------------------------->NEXT\n')
                        print '\n----->LEN: %d\n' % len(self.links_to_follow)
                        
                    #===============================================================
                    # except NameError,e:
                    #    print >>f, 'FIXME:',url,e
                    #    sys.exc_clear()
                    #    pass
                    # except mechanize.FormNotFoundError,e:
                    #    print >>f, 'FIXME:',url,e
                    #    sys.exc_clear()
                    #    pass
                    #===============================================================
                    
                    #===============================================================
                    # except mechanize.BrowserStateError,e:
                    #    assert str(e)== 'not viewing HTML'
                    #    print >>f, 'URL points to document! [',url,']'
                    #    #before getting next url from list, update:
                    #    f.write('**VISITED_URLS: %s \n' % url)
                    #    visited_urls.append(url)
                    #    f.write('Before_POP: len of links_to_follow: [%d]\n' % len(links_to_follow))
                    #    f.write('Pop: %s \n' % url)
                    #    links_to_follow.pop(links_to_follow.index(url))
                    #    f.write('After_POP: len of links_to_follow: [%d]\n' % len(links_to_follow))
                    #    f.write('--------------------------------------->NEXT\n')
                    #    print '\n----->LEN: %d\n' % len(links_to_follow)
                    #    pass
                    #===============================================================
                    
                    except Exception,e:
                    #except (URLError,InvalidURL,IndexError,mechanize.BrowserStateError),e:
                        try:
                            assert str(e)== 'not viewing HTML'
                            self._info('URL points to document! [',url,']')
                            self.crawler_log.write('URL points to document! ['+url+']')
                        finally:
                            self._info("Is this URL:",str(url)," valid?\n",str(e))
                            self.crawler_log.write("Is this URL:"+str(url)+" valid?\n"+str(e))
                        #before getting next url from list, update:
                        self.crawler_log.write('**VISITED_URLS: %s \n' % url)
                        _update_visited_list(self, url)
                        self.crawler_log.write('Before_POP: len of links_to_follow: [%d]\n' % len(self.links_to_follow))
                        self.crawler_log.write('Pop: %s \n' % url)
                        _delete_url_from_links_to_follow(self, url)
                        self.crawler_log.write('After_POP: len of links_to_follow: [%d]\n' % len(self.links_to_follow))
                        self.crawler_log.write('--------------------------------------->NEXT\n')
                        print '\n----->LEN: %d\n' % len(self.links_to_follow)
            
            self.crawler_log.write('>>>>>>>>>>>>>>>SCRIPT IS DONE\n')
            self._info('>>>>>>>>>>>>>>>SCRIPT IS DONE\n')
            self.crawler_log.write('Len of Visited_Links list: [%d] \n' % len(self.visited_urls))
            self._info('Len of Visited_Links list: [%d] \n' % len(self.visited_urls))
                

def main():
    obj = Crawler()
    obj.run_crawler()
    
if __name__ == '__main__':
    main()
    
    
    