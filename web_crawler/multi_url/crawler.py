import mechanize
import pprint
import re
import sys
import os
import urlparse
import loggers
import time
from multiprocessing import Process, Queue
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
    def __init__(self, start_url):
        self.links_to_follow = []
        self.visited_urls = []
        self.error_list = []
        self.start_url = start_url
        self.host_url = self._get_url_host(self.start_url)
        Get_Browser.__init__(self)
        #redirect sys.stdout (all print statements) to Logger obj
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
    
    def check_url_for_error(self, url, error_queue):
        response = self._opener.response()
        the_page = response.read()
        self._info("-->checking [%s] for errors... [page length: %d] " %(url,len(the_page)))
        search = re.search(r'(\w+\sis not available)|(Value does not fall within the expected range)', the_page)
        if search:
            self._warn('CHECK THIS URL:\n[%s]\n[%s]!\n' %(url, search.group(1)))
            self.error_list.append([url,search.group(1)])
            error_queue.put((self.net_loc, url, search.group(1)))
        else:
            self._info('no errors noticed\n')
                    
    def run_crawler(self, error_queue):
        def _update_visited_urls(self, url):
            self.visited_urls.append(url)
        def _update_links_to_follow(self, url):
            self.links_to_follow.append(url)
        def _delete_url_from_links_to_follow(self, url):
            self.links_to_follow.pop(self.links_to_follow.index(url))
        try:    
            self._info('Starting CWP_Web_Crawler ...\n\n')
            time.sleep(2)
            #start timer
            t0 = time.clock()
            #open start_url
            try:
                self._opener.open(self.start_url)
            except URLError,e:
                self._warn("is this URL: [",str(self.start_url),"] valid?\n",str(e))
                self.error_list.append([self.start_url,str(e)])
                #error_queue.put((self.net_loc, self.start_url , str(e)))
                sys.exit()
            #login to xnet
            try:
                self.login_to_xnet(username, passwd)
            except (mechanize.ControlNotFoundError,mechanize.FormNotFoundError),e:
                self._info('ALREADY LOGGED OR INET PAGE')
            #get all valid links
            finally:
                #check start_url for errors:
                self.check_url_for_error(self.start_url, error_queue)
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
                    self.check_url_for_error(url, error_queue)
                    self._info('>>scraping...')
                    for link in self._opener.links():
                        if link.url.startswith(self.host_url) or link.url.startswith('/') :
                            if link.url not in self.links_to_follow:
                                if link.url not in self.visited_urls:
                                    self._info('-->links_to_follow.append: %s ' % link.url)
                                    _update_links_to_follow(self, link.url)
                                else:
                                    self._info('-->skipping: %s ' % link.url)
                
                except mechanize.BrowserStateError,e:
                    if str(e)== 'not viewing HTML':
                        self._info('URL points to document! [',url,']')
                    else:
                        self._warn("is this URL: [",str(url),"] valid?\n",str(e))
                        self.error_list.append([url,str(e)])
                        #error_queue.put((self.net_loc, url, str(e)))
                
                except (URLError,InvalidURL,IndexError),e:
                    self._warn("is this URL:",str(url)," valid?\n",str(e))
                    self.error_list.append([url,str(e)])
                    #error_queue.put((self.net_loc, url, str(e)))
    
                finally:
                    #before getting next url from list, update:
                    _update_visited_urls(self, url)
                    self._info('-->link_to_follow.delete: %s ' % url)
                    _delete_url_from_links_to_follow(self, url)
                    
                    self._info('-->link_to_follow.length: [%d]' % len(self.links_to_follow))
                    self._info('-->visited_links.length: [%d] ' % len(self.visited_urls))
                    self._info('-->error_list.length: [%d] '%len(self.error_list))
                    #self._warn('error_list:')
                    #pprint.pprint(self.error_list)
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
            self._warn('Stopped by user!\nError list:\n')
            pprint.pprint(self.error_list)
            sys.exit()


def welcome_page():
        print ('>> Web_Crawler << author: Maciej Balazy >>')
        print INTRO
        time.sleep(2)

def get_url_list():
    print '\nChecking ['+crawler_start_file+ '] for url\'s start_list...'
    url_list = []
    with open(crawler_start_file, 'a+') as f:
        for line in f:
            if line.startswith('http'):
                url_list.append(line.strip())
        print '\nFollowing URLS will be checked: '
        pprint.pprint(url_list)
        ans = raw_input("\nSTART ? [y/n]")
        if ans == 'y':
            return url_list
        else:
            print 'User aborted execution...\n'
            sys.exit()
            
class menu(Crawler, RootClass):
   def __init__(self, start_url, error_queue):
       Crawler.__init__(self, start_url)
       self.run_crawler(error_queue)

def worker(url, error_queue):
    #to run from Run_Crawler.bat where you can provide start_url
    try:
        obj = menu(url, error_queue)
    finally:
        sys.stdout = sys.__stdout__     #revert sys.stdout to normal
        
#===============================================================================
# def worker(url, error_queue):
#    print 'inside worker'
#    time.sleep(2)
#    error_queue.put((url,'aaaa', 'ccc'))
#    print 'qsize: %d' % error_queue.qsize()
#    print 'empty: %s' % error_queue.empty()
#    print 'full: %s' % error_queue.full()
#===============================================================================
         
def writer_q2f(queue):
    '''
    every value appended to the error_queue in any of the running processes, has the same schema:
    (self.netloc, url, error) 
    '''
    #print 'inside writer'
    with open (common_log ,'a+') as f:
        while True: 
            try:
                host, url, error = queue.get(block=False)
                s = str(error)+' || '+str(host)+' || '+str(url)+'\n'
                print s
                f.write(s)
            except:
                break
            
def main():
    welcome_page()
    url_list = get_url_list()
    
    #all the started processes are appending error info to the common queue
    error_queue = Queue()
    jobs = []
    
    if url_list:
        for i in xrange(len(url_list)):
            process = Process(target=worker, args=(url_list[i], error_queue))
            print 'Starting process for ['+ url_list[i]+']'
            process.start()
            jobs.append(process)
            
        #===========================================================================
        # when all the processes are up and running, start 'listener' process, that 
        # gets as input 'error_queue' and writes all the items to the log file.
        # ->put listener in the infinite loop start/stop. Every time just check,
        # if there are any running jobs. If true: keep starting the 'listener', 
        # if false -> means that all jobs are done. (len(jobs)=0)
        #===========================================================================
        
        #=======================================================================
        # print '1',[job for job in jobs if job.is_alive()]
        # time.sleep(2)
        # print '2',[job for job in jobs if job.is_alive()]
        # time.sleep(2)
        # print '3',[job for job in jobs if job.is_alive()]
        # time.sleep(2)
        # print '4',[job for job in jobs if job.is_alive()]
        #=======================================================================
        
        while [job for job in jobs if job.is_alive()]:
           #print 'checking error_queue...'
           commonLog_proc = Process(target=writer_q2f, args=(error_queue,))
           commonLog_proc.start()
           time.sleep(120)
           commonLog_proc.join()
                 
        #when process is done, close gently:        
        for i in jobs:
            print '%s is %s' % (i.pid, i.is_alive())
            i.join()

if __name__ == '__main__':
    main()
        
    
    