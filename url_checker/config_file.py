import os,re
from time import strftime

#================== SPECIFIC TO URL_CHECKER =====================================
#
#current date
cur_date = strftime( "%y-%m-%d_%H_%M_%S_")

#current working dir
cwd = os.getcwd()

mechanize_headers = ('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3')

#PAC proxy file
proxy_path = os.path.join(cwd, 'proxy_conf')
pacfile = os.path.join(proxy_path,'proxyconf')              #PAC proxy file                          

#file with the list of urls to be checked
FILE_WITH_URLS = 'URLS.input'
input_file_path = os.path.join(cwd, 'input')
file_with_urls = os.path.join(input_file_path, FILE_WITH_URLS)

#filename of the report - always with extension!!
REPORT_NAME = 'CHECK_URLS.xls'
log_dir = os.path.join(cwd, 'logs')

#ensure that log dir exists:
not os.path.exists(log_dir) and os.makedirs(log_dir)
report_file = os.path.join(log_dir,cur_date+REPORT_NAME)

#DO NOT MODIFY ext_accept_list!
#list of acceptable report types (report file extension)
ext_accept_list = ['XLS','LOG']

#host files with ip_addr + server hosts files
PATH_HOSTS = 'C:\\WINDOWS\\system32\\drivers\\etc'
host_backUp = 'hosts_backUp'
host_original = 'hosts'     #this filename should correspond with actual 'host' filename 

#DO NOT MODIFY server pattern!
server_hosts_pattern = re.compile(r'^Server_hosts_\d{1}$')

#set TRUE to check URLs only through PROXY
run_URL_checks_through_PROXY = False

#provide login/pass:
username  = '*****'
passwd = '******'


INTRO = '''
>>>>>>  CWP_Urls_Checker  <<<<<<<

Script gets on the input list of urls, then creates requests and send them to predefined server.
Next, return code + IP_address of the actual host are logged to either log file or xls report.
Settings can be done via config_file.py

>> Scenario
Assume that all of your webpages are hosted on a couple of different servers (eg.S1,S2,S3,S4).
Your task is to ensure, that after each deploy, all the most important pages (and servers)
are up and running (you do not have direct access to the backend)
You've been given a complete list of the URLs that should be validated on each server.
-> config_file.py >> URLS.input
So, lets say that there are four host files with appropriate list of IP addresses (and corresponding host names)
-> see 'hosts' dir
These files are iteratively replaces with the original host file [C:\Windows\System32\drivers\etc\hosts]
(in my case, it ensures that requests actually hit proper server - bypassing proxy server)
and all the URLS are verified on every server.
Report file is saved with information about return code and eventual errors (see 'example_Input_Report' dir)
<<

For detailed info go to [%s/README] file
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
''' % cwd

