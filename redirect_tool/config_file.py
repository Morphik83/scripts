import os
from time import strftime

#current working dir
cwd = os.getcwd()

#current date
cur_date = strftime( "%y-%m-%d_%H_%M_%S_")

log_path = os.path.join(cwd, 'logs')
input_path = os.path.join(cwd, 'input')
proxy_path = os.path.join(cwd, 'proxy_conf')
proxy_url = 'http://<your_path_here>/'
proxy = os.path.join(proxy_path,'<proxy_pac_filename>')
headers = { 'User-Agent' : 'Mozilla/4.0'}
mechanize_headers = ('User-Agent','Mozilla/4.0')

pacfile = os.path.join(proxy_path,'proxy_pac_filename')              #PAC proxy file
input_file = os.path.join(input_path,'Redirects.input')                   #file with target/origin urls 

"""
graphic/detailed log - these logs presents only formatted sys.stdout!
There are no info whether the redirect is correct or not!
"""
graphic_log = os.path.join(log_path,cur_date+'Graphic_Redirect.log')               #graphic_log: GRAPHICAL representation of redirected urls
detailed_log = os.path.join(log_path,cur_date+'Detailed_Redirect.log')             #detailed_log: sys.stdout > detailed_log

"""
xls reports give the info about PASS/FAIL !
"""
xls_report = os.path.join(log_path,cur_date+'Redirects_Report_file.xls')           #xls_report: PASS/FAIL info in xls format 

INTRO = '''
>> Redirect_Tool v.1.0 << author: Maciej Balazy >>

NOTES: 
>Remember to add 'http://' to at least target_url!
>Valid input file must have following format:
    #comment (MANDATORY!)
    url_1<space>url_2    #url_1 ORIGIN URL, url_2 TARGET URL
    #url_1<space>url_2   #if line starts with '#' -> skip
    
INFO:
Redirects from [%s] will be verified 
LOGS will be saved in [%s] dir
'''% (input_file, log_path)
