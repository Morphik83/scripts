import os
from time import strftime

#current working dir
cwd = os.getcwd()

#current date
cur_date = strftime( "%y-%m-%d_%H_%M_%S_")

log_path = os.path.join(cwd, 'logs')
input_path = os.path.join(cwd, 'input')
proxy_path = os.path.join(cwd, 'proxy_conf')
headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3)'}

pacfile = os.path.join(proxy_path,'proxyconf')              #PAC proxy file
input_file = os.path.join(input_path,'Redirects.input')                   #file with target/origin urls 

"""
graphic/detailed log - these logs presents only formatted sys.stdout!
There are no info whether the redirect is correct or not!
"""
graphic_log = os.path.join(log_path,cur_date+'Graphic_Redirect.log')               #graphic_log: GRAPHICAL representation of redirected urls
detailed_log = os.path.join(log_path,cur_date+'Detailed_Redirect.log')             #detailed_log: sys.stdout > detailed_log

"""
final/xls reports give the info about PASS/FAIL !
"""
final_log = os.path.join(log_path,cur_date+'FINAL_Redirect.log')                   #final_log: PASS/FAIL info about each url
xls_report = os.path.join(log_path,cur_date+'Redirects_Report_file.xls')           #xls_report: PASS/FAIL info in xls format 

INTRO = '''
>> Redirect_Tool v.1.0 << author: Maciej Balazy >>

KNOWN ISSUES
1. if there are two (or more) the same origin_urls, only second one will be logged to xls report 
(dict cannot have two the same keys...)
 eg. www.volvoaero.com http://www.gkn.com/aerospace/pages/default.aspx
     www.volvoaero.com http://www.gkn.com/aerospace/pages/default.aspxa
2. http://www.volvotrucks.com http://www.volvotrucks.com
also does not work, since there is no redirection (missing 'TO' header, so there is no dict to compare results with)

NOTES: 
>Remember to add 'http://' to at least target_url!
>Valid input file must have following format:
    url_1<space>url_2    #url_1 ORIGIN URL, url_2 TARGET URL
    #url_1<space>url_2   #if line starts with '#' -> skip
    
INFO:
Redirects from [%s] will be verified 
LOGS will be saved in [%s] dir
'''% (input_file, log_path)
