import mechanize
from urllib2 import URLError
from httplib import InvalidURL
import pprint
import re
import sys
import os
import _root
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


class Get_Browser(object):
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
    
    def login_to_xnet(self,username, passwd):
        b.select_form(nr=0)
        b["ctl00$BodyContent$login$UserName"]=username
        b["ctl00$BodyContent$login$Password"]=passwd
        b.submit(name='ctl00$BodyContent$login$LoginButton')

class Run_URL_Checks(Get_Browser):
    
    def check_url_for_error(self, url,f):
        print '\n'
        response = self._browser.response()
        print ("Parsing opened page...")
        the_page = response.read()
        print("Checking [%s] for errors..." %url)
        f.write("Checking [%s] for errors... \n" %url)
        search = re.search('(not available)|(error)', the_page)
        if search:
            print('CHECK THIS URL [%s] !\n' %url)
        else:
            print('No errors noticed\n')

class Logs(object):
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
        self.start_url = start_url
        self.host_url = host_url
        Get_Browser.__init__(self)
        Logs.__init__(self, crawler_log, error_log)

    def run_crawler(self):
        
        def _update_visited_urls(self, url):
            self.visited_urls.append(url)
        def _update_links_to_follow(self, url):
            self.links_to_follow.append(url)
        def _delete_url_from_links_to_follow(self, url):
            self.links_to_follow.pop(self.links_to_follow.index(url))
            
        
        with self.crawler_log as f:
            #open start_url
            f.write('##OPEN %s \n' % self.start_url)
            self._browser.open(start_url)
            f.write('--->Checking for errors [%s]<---\n' %self.start_url)
            #login to xnet
            try:
                self.login_to_xnet(username, passwd)
            except mechanize.ControlNotFoundError,e:
                print 'ALREADY LOGGED'
            #get all valid links
            finally:
                for link in self._browser.links():
                    if link.url.startswith(self.host_url) or link.url.startswith('/') :
                        if link.url not in self.links_to_follow:
                            if link.url not in self.visited_urls:
                                f.write('--->links_to_follow.append: %s \n' % link.url)
                                _update_links_to_follow(link.url)
                            else:
                                f.write('--->skipping: %s \n' % link.url)
            
                _update_visited_urls(self.start_url)
                f.write('START: len of links_to_follow: [%d]\n' % len(self.links_to_follow))
                pprint.pprint(self.links_to_follow)
            
            while self.links_to_follow:
                try:
                    url = self.links_to_follow[0]
                    f.write('####NEXT URL: %s \n' % url)
                    self._browser.open(url)
                    f.write('--->Checking for errors [%s]<---\n' %url)
                    for link in self._browser.links():
                        if link.url.startswith(self.host_url) or link.url.startswith('/') :
                            if link.url not in self.links_to_follow:
                                if link.url not in self.visited_urls:
                                    f.write('--->links_to_follow.append: %s \n' % link.url)
                                    _update_links_to_follow(link.url)
                                else:
                                    f.write('--->skipping: %s \n' % link.url)
                    #before getting next url from list, update:
                    f.write('**VISITED_URLS: %s \n' % url)
                    _update_visited_urls(url)
                    f.write('Before_POP: len of links_to_follow: [%d]\n' % len(self.links_to_follow))
                    f.write('Pop: %s \n' % url)
                    _delete_url_from_links_to_follow(url)
                    f.write('After_POP: len of links_to_follow: [%d]\n' % len(self.links_to_follow))
                    f.write('--------------------------------------->NEXT\n')
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
                        print >>f, 'URL points to document! [',url,']'
                     
                    finally:
                        print >>f, "Is this URL:",str(url)," valid?\n",str(e)
                    
                    #before getting next url from list, update:
                    f.write('**VISITED_URLS: %s \n' % url)
                    self.visited_urls.append(url)
                    _update_visited_list(url)
                    f.write('Before_POP: len of links_to_follow: [%d]\n' % len(self.links_to_follow))
                    f.write('Pop: %s \n' % url)
                    _delete_url_from_links_to_follow(url)
                    f.write('After_POP: len of links_to_follow: [%d]\n' % len(self.links_to_follow))
                    f.write('--------------------------------------->NEXT\n')
                    print '\n----->LEN: %d\n' % len(self.links_to_follow)
            
            print >>f, '>>>>>>>>>>>>>>>SCRIPT IS DONE\n'
            print >>f, 'Len of Visited_Links list: [%d] \n' % len(self.visited_urls)
                

def main():
    pass
    
if __name__ == '__main__':
    #main()
    print 'test'