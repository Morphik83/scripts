import os

#================== SPECIFIC TO REDIRECT TOOL ===============================================================================
# 
PATH = 'D:\\tmp\\web_redirect_tool\\'
headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3)'}

pacfile = 'C:\\tmp\\proxyconf_srv_volvo_com'                          #PAC proxy file
input_file = os.path.join(PATH,'Redirects.input')                     #file with target/origin urls 

"""
graphic/detailed log - these logs presents only formatted sys.stdout!
There are no info whether the redirect is correct or not!
"""
graphic_log = os.path.join(PATH,'Graphic_Redirect.log')               #graphic_log: GRAPHICAL representation of redirected urls
detailed_log = os.path.join(PATH,'Detailed_Redirect.log')             #detailed_log: sys.stdout > detailed_log

"""
final/xls reports give the info about PASS/FAIL !
"""
final_log = os.path.join(PATH,'Final_Redirect.log')                   #final_log: PASS/FAIL info about each url
xls_report = os.path.join(PATH,'Redirects_Report_file.xls')           #xls_report: PASS/FAIL info in xls format

