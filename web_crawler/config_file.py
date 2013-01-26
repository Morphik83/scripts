import os
from credentials import *           #define username/passwd if needed 
from time import strftime

#current date
cur_date = strftime( "%y-%m-%d_%H_%M_%S_")

#headers for requests
headers = ('User-Agent','Mozilla/4.0')

#make sure that /logs dir exists
crawler_log_path = os.path.join(os.getcwd(),'logs')
not os.path.exists(crawler_log_path) and os.makedirs(crawler_log_path)
#CRAWLER.log path
crawler_log = os.path.join(crawler_log_path, cur_date+'CRAWLER.log')


#copy from README
INTRO = '''
>>>>> Web_Crawler <<<<<
Script traverses all the links within given host (url) and parses looking for the errors

How is this script working?
1. define start url (program asks when started)
2. start_url is opened and all the valid links from that page are scrapped. 
   Wait! VALID?
3. only links that have the same host as start_url (in our example 'http://online.renault-trucks-qa.volvo.com') 
   or links that start from '/' (so having the same host...) are added to check list (links_to_follow=[])
4. opened link is added to visited_urls = []
5. now, script is iterating over links_to_follow=[] and opening links one by one 
6. each opened page is scrapped for valid links (->having the host or starting from '/') and those links
   are appended to links_to_follow = [] (so the same list that script is iterating)
   Of course, every url before appended to links_to_follow=[] is checked if not exists in links_to_follow or 
   visited_links already to avoid checking page again!
7. opened link is deleted from links_to_follow and appended to visited_links
8. additionally, every opened page is checked for errors (see check_url_for_error method)
   ->this is very basic checking, but it is enough for me :)
9. if error is found on the page, such url is appended to error_list
10. eventually, there will be no more links having the same host that have not already been added to either 
   links_to_follow or visited_links lists. 
11. then links_to_follow list will start to shrink - next urls will be checked/opened and no new appends.
12. script is done when len(links_to_follow)=0

Pages with authentication are handled as well (see credentials in config_file.py) 

simplified logic:
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
start_url = 'http://online.renault-trucks-qa.volvo.com/dcs/tr/tr/Vente/Pages/VenteBOLD.aspx'
(so, only links that starts with 'http://online.renault-trucks-qa.volvo.com' or '/' will be checked)

links_to_follow = []
visited_urls = []
error_list = []

open start_url
    get_urls -> links_to_follow.append(urls)
    visisted_urls.append(start_url) 

for url in links_to_follow:
    open url
    get_urls -> if url not in links_to_follow and not in visited_urls:
                    links_to_follow.append(url)
                else:
                    skip url
                if url has errors:
                    error_list.append(url)   
    visited_urls.append(url)
    links_to_follow.pop(links_to_follow.index(url))
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
For example log file content see attached /logs/CRAWLER.log 
'''