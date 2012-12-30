import os,re
from time import strftime

#================== SPECIFIC TO URL_CHECKER ===============================================================================
#
#current date
cur_date = strftime( "%y-%m-%d_%H_%M_%S_")

#log dir/ input file location
PATH = 'D:\\tmp\\web_redirect_tool'

#headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3)'}
mechanize_headers = ('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3')

#file with the list of urls to be checked
FILE_WITH_URLS = 'URLS.input'
file_with_urls = os.path.join(PATH,FILE_WITH_URLS)

#filename of the report - always with extension!!
REPORT_NAME = 'CHECK_URLS.xls'
report_file = os.path.join(PATH,cur_date+REPORT_NAME)

#DO NOT MODIFY ext_accept_list!
#list of acceptable report types (report file extension)
ext_accept_list = ['XLS','LOG']

#host files with ip_addr + server hosts files
PATH_HOSTS = 'C:\\WINDOWS\\system32\\drivers\\etc'
host_backUp = 'hosts_backUp'
host_original = 'hosts'     #this filename should correspond with actual 'host' filename 

#DO NOT MODIFY server pattern!
server_hosts_pattern = re.compile(r'^SEGOTN\d{4}$|^AKAMAI(.*)$|^PROXY(.*)$')

#set True/False wheather you want to check all the subpages on given page
#set TRUE  if all the links from given page should be checked as well 
#    (eg. http://volovit.com -> any link that exists on that page will be checked) 
#set FALSE if only pages from URLS.input file should be checked
check_all_subPages = True

#Not implemented yet!
#run_URL_checks_through_PROXY = False


#provide login/pass for xnet pages:
username  = '******'
passwd = '*****'

