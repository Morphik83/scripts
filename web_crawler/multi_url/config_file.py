import os
from credentials import *           #define username/passwd if needed 
from time import strftime

#current working dir
cwd = os.getcwd()

#current date
cur_date = strftime( "%y-%m-%d_%H_%M_%S_")

#headers for requests
headers = ('User-Agent','Mozilla/4.0')

#make sure that /logs dir exists
crawler_log_path = os.path.join(cwd,'logs')
not os.path.exists(crawler_log_path) and os.makedirs(crawler_log_path)

#CRAWLER.log path
crawler_log = os.path.join(crawler_log_path, cur_date+'CRAWLER.log')

#COMMON.log path
#keep the same name,do not append cur_date, since
#we are appending to that log in the loop! We want one log, to milion of them!
common_log = os.path.join(crawler_log_path, 'COMMON_ERROR.log') 

#url_list input file
input_log_path = os.path.join(cwd,'input')
crawler_start_file = os.path.join(input_log_path, 'crawler_start_file')
#make sure /input dir exists
not os.path.exists(input_log_path) and os.makedirs(input_log_path)

#copy from README
INTRO = '''
>>>>> Web_Crawler <<<<<
Script traverses all the links within given host (url) and parses looking for the errors

How is this script working?
1. define list of valid (starting from http://) url addresses in the /input dir (crawler_start_file)
2. there will separate process started for each start_url address from crawler_start_file
3. start_url is opened and all the valid links from that page are scrapped. 
   Wait! VALID?
4. only links that have the same host as start_url (in the example 'http://github.com') 
   or links that start from '/' (so having the same host...) are added to check list (links_to_follow=[])
5. opened link is added to visited_urls = []
6. now, script is iterating over links_to_follow=[] and opening links one by one 
7. each opened page is scrapped for valid links (->having the host or starting from '/') and those links
   are appended to links_to_follow = [] (so the same list that script is iterating)
   Of course, every url before appended to links_to_follow=[] is checked if not exists in links_to_follow or 
   visited_links already to avoid checking page again!
8. opened link is deleted from links_to_follow and appended to visited_links
9. additionally, every opened page is checked for errors (see check_url_for_error method)
   ->this is very basic checking, but it is enough for me :)
10. if error is found on the page, such url is appended to error_list
11. eventually, there will be no more links having the same host that have not already been added to either 
   links_to_follow or visited_links lists. 
12. then links_to_follow list will start to shrink - next urls will be checked/opened and no new appends.
13. script is done when len(links_to_follow)=0

14. When all the processes are running, then concurrently last process starts up and cleans the error_queue by 
writing each and every element to 'COMMON_ERROR.log'

Pages with authentication are handled as well (see credentials in config_file.py) 

simplified logic:
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
start_url = 'http://github.com'
(so, only links that starts with 'http://github.com' or '/' will be checked)

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
For example log file content see attached /logs/[github.com]13-01-31_13_38_56_CRAWLER.log
'''