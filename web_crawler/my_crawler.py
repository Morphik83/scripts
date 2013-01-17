import mechanize
from urllib2 import URLError
from httplib import InvalidURL
import pprint
import re
import sys
import os

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


#host_url = 'http://online.renault-trucks-qa.volvo.com'
host_url = 'http://volvogroup.com/group/global/en-gb'
start_url = 'http://volvogroup.com/group/global/en-gb/Pages/group_home.aspx'
#start_url = 'http://online.renault-trucks-qa.volvo.com'
headers = ('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3')

crawler_log_path = os.path.join(os.getcwd(),'logs')
crawler_log = os.path.join(crawler_log_path, 'CRAWLER.log')

username = '****'
passwd = '******'

b = mechanize.Browser()
b.set_debug_http(True)
b.set_handle_robots(False)
b.set_debug_redirects(True)
b.set_debug_responses(True)
b.addheaders=[headers]

visited_urls = []
links_to_follow = []

def main():
    with open(crawler_log,'a+') as f:
        #open start_url
        f.write('##OPEN %s \n' % start_url)
        b.open(start_url)
        f.write('--->Checking for errors [%s]<---\n' %start_url)
        #login to xnet
        try:
            login_to_xnet(username, passwd)
        except mechanize.ControlNotFoundError,e:
            print 'ALREADY LOGGED'
        #get all valid links
        finally:
            for link in b.links():
                if link.url.startswith(host_url) or link.url.startswith('/') :
                    if link.url not in links_to_follow:
                        if link.url not in visited_urls:
                            f.write('--->links_to_follow.append: %s \n' % link.url)
                            links_to_follow.append(link.url)
        
            visited_urls.append(start_url)
            f.write('START: len of links_to_follow: [%d]\n' % len(links_to_follow))
            pprint.pprint(links_to_follow)
        
        while links_to_follow:
            try:
                url = links_to_follow[0]
                f.write('####NEXT URL: %s \n' % url)
                b.open(url)
                f.write('--->Checking for errors [%s]<---\n' %url)
                for link in b.links():
                    if link.url.startswith(host_url) or link.url.startswith('/') :
                        if link.url not in links_to_follow:
                            if link.url not in visited_urls:
                                f.write('--->links_to_follow.append: %s \n' % link.url)
                                links_to_follow.append(link.url)
                            else:
                                f.write('--->skipping: %s \n' % link.url)
                #before getting next url from list, update:
                f.write('**VISITED_URLS: %s \n' % url)
                visited_urls.append(url)
                f.write('Before_POP: len of links_to_follow: [%d]\n' % len(links_to_follow))
                f.write('Pop: %s \n' % url)
                links_to_follow.pop(links_to_follow.index(url))
                f.write('After_POP: len of links_to_follow: [%d]\n' % len(links_to_follow))
                f.write('--------------------------------------->NEXT\n')
                print '\n----->LEN: %d\n' % len(links_to_follow)
                
            except NameError,e:
                print >>f, 'FIXME:',url,e
                sys.exc_clear()
                pass
            except mechanize.FormNotFoundError,e:
                print >>f, 'FIXME:',url,e
                sys.exc_clear()
                pass
            except mechanize.BrowserStateError,e:
                assert str(e)== 'not viewing HTML'
                print >>f, 'URL points to document! [',url,']'
                #before getting next url from list, update:
                f.write('**VISITED_URLS: %s \n' % url)
                visited_urls.append(url)
                f.write('Before_POP: len of links_to_follow: [%d]\n' % len(links_to_follow))
                f.write('Pop: %s \n' % url)
                links_to_follow.pop(links_to_follow.index(url))
                f.write('After_POP: len of links_to_follow: [%d]\n' % len(links_to_follow))
                f.write('--------------------------------------->NEXT\n')
                print '\n----->LEN: %d\n' % len(links_to_follow)
                pass
            except (URLError,InvalidURL,IndexError),e:
                print >>f, "Is this URL:",str(url)," valid?\n",str(e)
                #sys.exc_clear()
                #before getting next url from list, update:
                f.write('**VISITED_URLS: %s \n' % url)
                visited_urls.append(url)
                f.write('Before_POP: len of links_to_follow: [%d]\n' % len(links_to_follow))
                f.write('Pop: %s \n' % url)
                links_to_follow.pop(links_to_follow.index(url))
                f.write('After_POP: len of links_to_follow: [%d]\n' % len(links_to_follow))
                f.write('--------------------------------------->NEXT\n')
                print '\n----->LEN: %d\n' % len(links_to_follow)
        
        print >>f, '>>>>>>>>>>>>>>>SCRIPT IS DONE\n'
        print >>f, 'Len of Visited_Links list: [%d] \n' % len(visited_urls)
                
def check_url_for_error(url,f):
        print '\n'
        response = b.response()
        print ("Parsing opened page...")
        the_page = response.read()
        print("Checking [%s] for errors..." %url)
        f.write("Checking [%s] for errors... \n" %url)
        search = re.search('(not available)|(error)', the_page)
        if search:
            print('CHECK THIS URL [%s] !\n' %url)
        else:
            print('No errors noticed\n')
            
def login_to_xnet(username, passwd):
    b.select_form(nr=0)
    b["ctl00$BodyContent$login$UserName"]=username
    b["ctl00$BodyContent$login$Password"]=passwd
    b.submit(name='ctl00$BodyContent$login$LoginButton')



if __name__ == '__main__':
    main()