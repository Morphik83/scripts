#from fetchURL_byProxy import fetchurl,isproxyalive
from output_parser import *
from config_file import *

"""
For detailed config, see config_file.py!

NOTE:
There are four logs created (graphic AND detailed,  final OR xls), 
but only final/xls logs give the info about PASS/FAIL !!
graphic/detailed presents only formatted sys.stdout !!
"""


"""
KNOWN ISSUES
1. if there are two (or more) the same origin_urls, only second one will be logged to xls report 
(dict cannot have two the same keys...)
 eg. www.volvoaero.com http://www.gkn.com/aerospace/pages/default.aspx
     www.volvoaero.com http://www.gkn.com/aerospace/pages/default.aspxa
2. http://www.volvotrucks.com http://www.volvotrucks.com
also does not work, since there is no redirection (missing 'TO' header, so there is no dict to compare results with)
"""


def input_data(input_file):
    """
    Valid input file must have following format:
    url_1<space>url_2    #url_1 ORIGIN URL, url_2 TARGET URL
    #url_1<space>url_2   #if line starts with '#' -> skip
    """    
    redirects_input_file = open(input_file, 'r+')
    in_list = [] #list for INPUT urls
    out_list = [] #list for target urls
    redirect_dict = {}
    
    searchPattern = re.compile(r'(^[^\/#].*?)\s(.*$)')  # in reg_exp ? is used for non-greedy search pattern - without ?, first match will cover whole line (up to $) due to .*
    for line in redirects_input_file:
        search = re.search(searchPattern, line)
        if search:
            #print "1: ",search.group(1)
            url_in = search.group(1)
            if not re.match(r'^http[s]?://',search.group(1)):
                url_in = 'http://'+search.group(1)
            in_list.append(url_in)
            
            #print "2: ",search.group(2)
            url_out = search.group(2)
            '''
            I had to turn-off adding 'http' to the target_url(below) 
            in order to allow proper checking of the Xnet Login pages
            eg. current behavior: http://www.trucksdealerportal.com -> /_layouts/login.aspx?ReturnUrl=%2f
            but with enabled 'http' append it was like below:
            http://www.trucksdealerportal.com -> http:///_layouts/login.aspx?ReturnUrl=%2f
            As the side-effect, it is now required to manually add 'http' to the target_ur where needed
            '''
            #===================================================================
            # if not re.match(r'^http[s]?://',search.group(2)):
            #   url_out = 'http://'+search.group(2)
            # out_list.append(url_out)
            #===================================================================
            
            redirect_dict[url_in] = url_out
            
    return in_list,out_list,redirect_dict

def fetch_url(redirects_list):
    """
    by using 'fetchurl' we connect to network by PAC proxy file
    setting http_debuglevel=1 in fetchurl causes all the detailed info to be displayed on sys.stdout 
    (but we redirected that stream to 'logger', so all the data is being saved in logger.content as well) 
    """
    
    logger = loggers.Logger(detailed_log)       #creates DefaultLog (DEBUG log) file - see in Logger obj for details
    sys.stdout = logger                         #redirect all the outputs to the logger obj
                                
    try:
        for url in redirects_list[0]:           #loop over in_list --> (redirects_list[0])
            print ">>>>ORIGIN_URL:"+url         #needed for proper output parsing (marker of the request beginning)
                                                #+ -> to keep everything in one line in sys.stdout
            #>>>====AT HOME ONLY - NO PROXY!===================================
            handler = urllib2.HTTPHandler()
            handler.set_http_debuglevel(1)
            #cookie = urllib2.HTTPCookieProcessor()
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
            request = urllib2.Request(url, None, headers)
            #<<<===============================================================
            
            try:
                #fetchurl(pacfile, url, headers)
                #>>>====AT HOME ONLY - NO PROXY!================================
                opener.open(request)
                #<<<============================================================
            except URLError, e:                     #invalid URL
                print "ERROR: "+url+" This URL does not exist! " + str(e)
            except ValueError, e:                   #url without 'http://'
                if re.search(r'unknown url type', str(e)):
                    try:
                        #fetchurl(pacfile, 'http://'+url)
                        #>>>====AT HOME ONLY - NO PROXY!========================
                        request = urllib2.Request('http://'+url, None, headers)
                        opener.open(request)
                        #<<<====================================================
                    except Exception, e:                     #still might be invalid URL, eg.'ww.volvo.com'
                        print "ERROR: "+url+" This URL does not exist! " + str(e)
            
    finally:
        sys.stdout = sys.__stdout__                 #revert sys.stdout to normal
    return logger.content

def run():
    
    #get list of URLs to check redirects (from input_file)
    redirects_list = input_data(input_file)
    
    #create url_requests and save all the data to .content variable
    log_content = fetch_url(redirects_list)
    
    #when all the URLs are already opened/redirected and all the outputs are written to logger.content
    #lets generate graphic_log file
    parser = Output_Parser(log_content, graphic_log)
    out_dict = parser.generate_output()
    
    #Finally, lets check if all redirects are correct and generate final_log (LOG or XLS)
    parser.verify_redirects(redirects_list, out_dict, 'xls')

def main():
    print INTRO
    ans = raw_input('START [y/n]? ')
    if ans == 'y':
        print 'Starting...\n'
        time.sleep(2)
        run()
    else:
        print 'Exiting...'
        sys.exit()

if __name__ == '__main__':
    main()

    #===========================================================================
    # import os
    # path = 'C:\\testing\\redirects\\cmd_redirect_tool\\'
    # headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3)'}
    # pacfile = 'C:\\tmp\\proxyconf_srv_volvo_com'           #PAC proxy file
    # input_file = os.path.join(path,'Redirects.input')
    # 
    # print input_file  
    #===========================================================================
