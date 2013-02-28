import mechanize
import pprint
import re
import sys
import os
import urlparse
import loggers
import time
import win32com.client
from multiprocessing import Process, Queue
from _root import *
from config_file import * 
from urllib2 import URLError
from httplib import InvalidURL

class Get_Browser(RootClass):
    """creates browser's instance; feeds CheckURLs
    """
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
        """inserts start_url hostname to the crawler log file
        before: D:\workspace\Git\scripts\web_crawler\logs\13-01-31_13_22_45_CRAWLER.log
        after:  D:\workspace\Git\scripts\web_crawler\logs\[volvo.com]13-01-31_13_22_45_CRAWLER.log
        """
        pttrn = re.compile(r'(.*\\)(.*$)')
        result = re.search(pttrn, crawler_log)
        if result:
            return result.group(1)+'['+self.net_loc+']'+result.group(2)
        else:
            self._warn('add_hostname_to_crawler_log: Cannot add hostname to the crawler_log!')
            
    def _get_url_host(self,url):
        self._info('Getting host from [%s]' % url)
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
        errorList = [r'(\w+\sis not available)',\
                     r'(Value does not fall within the expected range)',\
                     r'(Field type CWPRichText is not installed properly)',\
                     r'(at Microsoft.SharePoint.\.*)',]
        
        response = self._opener.response()
        the_page = response.read()
        self._info("-->checking [%s] for errors... [page length: %d] " %(url,len(the_page)))
        
        if url not in self.error_list:   #to avoid appending the same url twice
            for error in errorList:
                search = re.search(error, the_page)
                if search:
                    self._warn('CHECK THIS URL:\n[%s]\n[%s]!\n' %(url, search.group(1)))
                    self.error_list.append([url,search.group(1)])
                    error_queue.put((self.net_loc, url, search.group(1)))
                else:
                    self._info('no errors noticed\n')
                    
    def run_crawler(self, error_queue):
        try:    
            self._info('Starting CWP_Web_Crawler ...\n\n')
            time.sleep(1)
            #start timer
            t0 = time.clock()
            #open start_url
            try:
                if not re.search(r'[?]', self.start_url):   #to exclude urls with query strings
                    self._opener.open(self.start_url)
                else:
                    self._info('-->skipping(urlsWithQueryStr>"?"): %s ' % self.start_url)
                    sys.exit()
            except URLError,e:
                self._warn("is this URL: [",str(self.start_url),"] valid?\n",str(e))
                self.error_list.append([self.start_url,str(e)])
                sys.exit()
            #login to xnet
            try:
                self.login_to_xnet(username, passwd)
            except (mechanize.ControlNotFoundError,mechanize.FormNotFoundError),e:
                self._info('ALREADY LOGGED OR INET PAGE')
            #get all valid links
            finally:
                self.check_url_for_error(self.start_url, error_queue)   #check for errors:
                self._info('>>scraping...')
                for link in self._opener.links():
                    if not re.search(r'[?]', link.url):   #to exclude urls with query strings
                        if link.url.startswith(self.host_url) or link.url.startswith('/') :
                            if link.url not in self.links_to_follow:
                                if link.url not in self.visited_urls:
                                    self._info('-->links_to_follow.append: %s ' % link.url)
                                    self.links_to_follow.append(link.url)
                                else:
                                    self._info('-->skipping: %s ' % link.url)
                    else:
                        self._info('-->skipping(urlsWithQueryStr>"?"): %s ' % link.url)           
                self.visited_urls.append(self.start_url)
                self._info('-->link_to_follow.length: [%d]' % len(self.links_to_follow))
                print '\n'
                self._info('------------------->> NEXT <<-------------------')
                
            while self.links_to_follow:
                try:
                    url = self.links_to_follow[0]
                    self._info('>>opening: [%s] \n' % url)
                    
                    self._opener.open(url)
                    self.check_url_for_error(url, error_queue)  #check for error:
                    self._info('>>scraping...')
                    for link in self._opener.links():
                        if not re.search(r'[?]', link.url):   #to exclude urls with query strings
                            if link.url.startswith(self.host_url) or link.url.startswith('/'):
                                if link.url not in self.links_to_follow:
                                    if link.url not in self.visited_urls:
                                        self._info('-->links_to_follow.append: %s ' % link.url)
                                        self.links_to_follow.append(link.url)
                                    else:
                                        self._info('-->skipping(alreadyVisited|addedToFollow: %s ' % link.url)
                            else:
                                self._info('-->skipping (notStartWith hostname or /: %s ' % link.url)
                        else:
                            self._info('-->skipping(urlsWithQueryStr): %s ' % link.url)
                
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
                    self.visited_urls.append(url)
                    self._info('-->link_to_follow.delete: %s ' % url)
                    self.links_to_follow.pop(self.links_to_follow.index(url))
                    
                    self._info('-->link_to_follow.length: [%d]' % len(self.links_to_follow))
                    self._info('-->visited_links.length: [%d] ' % len(self.visited_urls))
                    self._info('-->error_list.length: [%d] '%len(self.error_list))
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
            self._warn('>>'+strftime("%H:%M:%S")+'<< Stopped by user!\nError list:\n')
            pprint.pprint(self.error_list)
            sys.exit()

def welcome_page():
        print ('>> Web_Crawler << author: Maciej Balazy >>\n\n')
        #print INTRO
        time.sleep(1)

def get_url_list():
    print '\nChecking ['+crawler_start_file+ '] for url\'s start_list...'
    url_list = []
    with open(crawler_start_file, 'a+') as f:
        for line in f:
            if line.startswith('http'):
                url_list.append(line.strip())
        print '\nFollowing URLS will be checked: '
        pprint.pprint(url_list)
        ans = raw_input("\nSTART ? [y/n] ")
        if ans == 'y':
            return url_list
        else:
            print 'User aborted execution...\n'
            sys.exit()

def get_email_addresses():
    addr_to = raw_input('Enter valid e-mail address [to]: ')
    if re.search(r'[@]',addr_to):
        to=addr_to
    else:
        to=None
        print 'E-mail address not valid! Cannot send e-mail!'
    
    addr_cc = raw_input('Enter valid e-mail address [cc]: ')
    if re.search(r'[@]',addr_cc):
        cc=addr_cc
    else:
        cc=None
        print 'Ohh come on! Is this really correct e-mail[cc] ? :)'
    
    return to,cc
    
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
    """every value appended to the error_queue in any of the running processes, has the same schema:
    (self.netloc, url, error) 
    """
    with open (common_log ,'a+') as f:
        while True: 
            try:
                host, url, error = queue.get(block=False)
                s = '\n'+str(error)+' || '+str(host)+str(url)
                print s
                f.write(s)
            except:
                break

def send_mail(**kwargs):
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
    def _checkError_queue():
        commonLog_proc = Process(target=writer_q2f, args=(error_queue,))
        commonLog_proc.start()
        print '\n>>'+strftime("%H:%M:%S")+'<< Checking error_queue...'
        time.sleep(5)
        print '\n>>'+strftime("%H:%M:%S")+'<< Checking error_queue - Done'
        print '\n>>'+strftime("%H:%M:%S")+'<< Script is running...\nKeep checking logs [%s]\n' % crawler_log_path
        commonLog_proc.terminate()
        commonLog_proc.join()
    try:
        welcome_page()
        to_email, cc_email = get_email_addresses()
        url_list = get_url_list()
        
        #all the started processes are appending error info to the common queue
        error_queue = Queue()
        #IDs of the dispatched processes are stored here 
        jobs = []
        #monitor is used to track active jobs - if not, send_mail with results
        monitor = {}
        
        if url_list:
            for i in xrange(len(url_list)):
                process = Process(target=worker, args=(url_list[i], error_queue))
                print '>>'+strftime("%H:%M:%S")+'<< Starting process for ['+ url_list[i]+']'
                process.start()
                jobs.append(process)
                monitor[process]= url_list[i]
                
            """
            when all the processes are up and running, start 'listener' process, that 
            gets as input 'error_queue' and writes all the items to the log file.
            ->put listener in the infinite loop start/stop (as long as there is at least
            one active job). 
            If true: keep starting the 'listener', 
            if false -> means that all jobs are done. (len(jobs)=0)
            """
            
            while [job for job in jobs if job.is_alive()]:
                active_jobs_list = [job for job in jobs if job.is_alive()]
                #print '\n>>'+strftime("%H:%M:%S")+'<< ACTIVE_JOBS: '
                #pprint.pprint (active_jobs_list)
                print '\n>>'+strftime("%H:%M:%S")+'<< MONITOR: '
                pprint.pprint(monitor)
                
                for job_process in monitor.keys():
                    if job_process not in active_jobs_list:
           
                        print str('\n\n>>'+strftime("%H:%M:%S")+'<< '+monitor[job_process]+'>>Crawler has finished!')
                        print '>>'+strftime("%H:%M:%S")+'<< Check common_log for error [%s]\n\n' %common_log
           
                        if to_email and not cc_email:        #send_mail only if to_mail given
                            send_mail(To=to_email, Subject=str(monitor[job_process]+' >>Crawler has finished!')\
                                      ,Body='[1]CommonLog attached', Attachments=common_log)
                        if to_email and cc_email:
                            send_mail(To=to_email, Cc=cc_email, Subject=str(monitor[job_process]+' >>Crawler has finished!')\
                                      ,Body='[1]CommonLog attached', Attachments=common_log)
                        
                        job_process.terminate()
                        job_process.join()
                        monitor.pop(job_process)
           
                """
                example:
                active jobs list: 
                [<Process(Process-1, started)>, 
                <Process(Process-2, started)>, 
                <Process(Process-3, started)>,]
                
                MONITOR: 
                {<Process(Process-1, started)>: 'http://volvoitxnet-qa.volvo.com', 
                <Process(Process-2, started)>: 'http://vfsco-qa.volvo.com', 
                <Process(Process-3, started)>: 'http://volvobuses-qa.volvo.com',}
                """
            
                """
                check error_queue in 5 minutes cycles and if not-empty, write to common_log
                """
                _checkError_queue()
                time.sleep(300)
            
            """
            when all the processes are done, check error_queue last time 
            (in case script was finished before time.sleep() passes - then 
            eventual items from error_queue would not be saved to the commonLog
            """
            _checkError_queue()
                   
            #when process is done, close gently:        
            for i in jobs:
                print '%s is %s' % (i.pid, i.is_alive())
                i.join()
            
            """
            send_mail only when all the jobs are done with truly common_log ;)
            """
            if to_email and not cc_email:    #send_mail only if to_mail given
                send_mail(To=to_email, Subject=str(monitor[job_process]+' >>Crawler has finished!')\
                          ,Body='[2]CommonLog attached', Attachments=common_log) 
            if to_email and cc_email:    #send_mail only if to_mail given
                send_mail(To=to_email, Cc=cc_email, Subject=str(monitor[job_process]+' >>Crawler has finished!')\
                          ,Body='[2]CommonLog attached', Attachments=common_log)
            print '>>'+strftime("%H:%M:%S")+'<< Crawler has finished!<<'
            print '>>'+strftime("%H:%M:%S")+'<< Check common_log for error [%s]\n' %common_log
    
    except KeyboardInterrupt:
        print '\n'
        _checkError_queue()
        print ('>>'+strftime("%H:%M:%S")+'<< Terminated by user!')
        sys.exit()
        
if __name__ == '__main__':
   main()
   