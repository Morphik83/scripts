import os

#================== SPECIFIC TO URL_CHECKER ===============================================================================
#
PATH = 'D:\\tmp\\web_redirect_tool\\'
headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3)'}

#file with the list of urls to be checked
FILE_WITH_URLS = 'URLS.input'
file_with_urls = os.path.join(PATH,FILE_WITH_URLS)

#filename of the report - always with extension!!
REPORT_NAME = 'CHECK_URLS.xls'
report_file = os.path.join(PATH,REPORT_NAME)

#list of acceptable report types (report file extension)
ext_accept_list = ['XLS','LOG']

#host files with ip_addr + server
SERVER_1 = "SEGOTN2525" 
SERVER_2 = "SEGOTN2543"
SERVER_3 = "SEGOTN2553"
SERVER_4 = "SEGOTN2544"
host_Server_1 = os.path.join(PATH,SERVER_1)
host_Server_2 = os.path.join(PATH,SERVER_2)
host_Server_3 = os.path.join(PATH,SERVER_3)
host_Server_4 = os.path.join(PATH,SERVER_4)

