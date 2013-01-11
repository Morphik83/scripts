import os,re
from time import strftime

#================== SPECIFIC TO URL_CHECKER ===============================================================================
#
#current date
cur_date = strftime( "%y-%m-%d_%H_%M_%S_")

#log dir/ input file location
PATH = 'D:\\tmp\\url_checker'

mechanize_headers = ('User-Agent','Mozilla/4.0')

#PAC proxy file
pacfile = '<yout PAC file here>'                          

#file with the list of urls to be checked
FILE_WITH_URLS = 'URLS.input'
file_with_urls = os.path.join(PATH,FILE_WITH_URLS)

#filename of the report - always with extension!!
REPORT_NAME = 'CHECK_URLS.xls'
log_dir = os.path.join(PATH, 'logs')
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

#provide login/pass for xnet pages:
username  = '******'
passwd = '******'