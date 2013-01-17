import os


start_url = 'http://volvogroup.com/group/global/en-gb/Pages/group_home.aspx'
host_url = 'http://volvogroup.com'
headers = ('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3')



username = '*****'
passwd = '******'


crawler_log_path = os.path.join(os.getcwd(),'logs')
crawler_log = os.path.join(crawler_log_path, 'CRAWLER.log')
error_log = os.path.join(crawler_log_path, 'CRAWLER_ERROR.log')