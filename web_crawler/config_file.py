import os
from credentials import *


#start_url = 'http://volvogroup.com/group/global/en-gb/Pages/group_home.aspx'
start_url = 'http://online.renault-trucks.com'
headers = ('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3')

crawler_log_path = os.path.join(os.getcwd(),'logs')
#make sure that /logs dir exists:
not os.path.exists(crawler_log_path) and os.makedirs(crawler_log_path)
crawler_log = os.path.join(crawler_log_path, 'CRAWLER.log')
error_log   = os.path.join(crawler_log_path, 'CRAWLER_ERROR.log')