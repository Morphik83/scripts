import os
from credentials import *           #define username/passwd if needed 

#exampoe start_url
start_url = 'http://gazetapraca.pl/0,0.html#NavPion'

#headers for requests
headers = ('User-Agent','Mozilla/4.0')

#make sure that /logs dir exists
crawler_log_path = os.path.join(os.getcwd(),'logs')
not os.path.exists(crawler_log_path) and os.makedirs(crawler_log_path)
#CRAWLER.log path
crawler_log = os.path.join(crawler_log_path, 'CRAWLER.log')
