from fetchURL_byProxy import fetchurl,isproxyalive
from output_parser import *
from config_file import *
import win32com.client
import mechanize
import os

def input_data(input_file):
    """
    Valid input file must have following format:
    #Mandatory Comment!!
    url_1<spaces>url_2    
    url_3<spaces>url_4
    
    Where: url_1/3->ORIGIN URL, url_2/4->TARGET URL
        
    I had to turn-off adding 'http' to the target_url(below) 
    in order to allow proper checking of the Xnet Login pages
    eg. current behavior: http://www.trucksdealerportal.com -> /_layouts/login.aspx?ReturnUrl=%2f
    but with enabled 'http' append it was like below:
    http://www.trucksdealerportal.com -> http:///_layouts/login.aspx?ReturnUrl=%2f
    As the side-effect, it is now required to manually add 'http' to the target_url where needed
    """
    redirects_input_file = open(input_file, 'r+')
    input_list = []
    in_list = [] #list for INPUT urls
    
    searchComment = re.compile(r'^\s*#(.*)')
    searchURLS = re.compile(r'^([^#].*?)\s+(.*$)')  # in reg_exp ? is used for non-greedy search pattern - without ?, first match will cover whole line (up to $) due to .*
    
    for line in redirects_input_file:
        urls = re.search(searchURLS, line)
        comment = re.search(searchComment, line)
        if comment:
            test_comment =  comment.group(1)
            input_list.append([comment.group(1)])
        if urls:
            url_in = urls.group(1)
            if not re.match(r'^http[s]?://',urls.group(1)):
                url_in = 'http://'+urls.group(1)
            in_list.append(url_in)
            url_out = urls.group(2)
            for x in xrange(len(input_list)):
                if input_list[x][0] == test_comment:
                    input_list[x].append((url_in,url_out))
    """
    input_list looks like:
    example output:
        input_list[0] =>['comment_1', ('url_1', 'url_2')]
        input_list[1] =>['comment_2', ('url_3', 'url_4'), ('url_5', 'url_6')]
    """
    return in_list,input_list

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
            #handler = urllib2.HTTPHandler()
            #handler.set_http_debuglevel(1)
            #cookie = urllib2.HTTPCookieProcessor()
            #opener = urllib2.build_opener(handler)
            #urllib2.install_opener(opener)
            #request = urllib2.Request(url, None, headers)
            #<<<===============================================================
            
            try:
                fetchurl(pacfile, url, headers)
                #>>>====AT HOME ONLY - NO PROXY!================================
                #opener.open(request)
                #<<<============================================================
            except URLError, e:                     #invalid URL
                print "ERROR: "+url+" This URL does not exist! " + str(e)
            except ValueError, e:                   #url without 'http://'
                if re.search(r'unknown url type', str(e)):
                    try:
                        fetchurl(pacfile, 'http://'+url)
                        #>>>====AT HOME ONLY - NO PROXY!========================
                        #request = urllib2.Request('http://'+url, None, headers)
                        #opener.open(request)
                        #<<<====================================================
                    except Exception, e:                     #still might be invalid URL, eg.'ww.volvo.com'
                        print "ERROR: "+url+" This URL does not exist! " + str(e)
            
    finally:
        sys.stdout = sys.__stdout__                 #revert sys.stdout to normal
    return logger.content

def send_mail(**kwargs):
        """available args:
        [to,cc,bcc,body,subject,attachment]
        pass arguments as below:
        (Cc='this_is_cc',Body='this_is_body', to='test@test.test')
        """
        MailItem = 0x0
        outlook = win32com.client.Dispatch("Outlook.Application")
        newMail = outlook.CreateItem(MailItem)
        
        for key in kwargs:
            if re.search(r'[Tt]o',key):
                newMail.To = kwargs[key]
            elif re.search(r'[Cc]c',key):
                newMail.CC = kwargs[key]
            elif re.search(r'[Bb]cc',key):
                newMail.Bcc = kwargs[key]
            elif re.search(r'[Ss]ubject', key):
                newMail.Subject = kwargs[key]
            elif re.search(r'[Bb]ody',key):
                newMail.Body = kwargs[key]
            elif re.search(r'[Aa]ttachments',key):
                #iterate over list of attachments
                lst_with_attchments = kwargs[key]
                for attch in lst_with_attchments: 
                    newMail.Attachments.Add(attch)
            else:
                print '>>'+strftime("%H:%M:%S")+' Send_mail: incorrect key! [%s]' % key
        #newMail.display()
        newMail.Send()
        
        print '>>'+strftime("%H:%M:%S")+'<< Email with the results sent to the recipients!'
        
def get_email_addresses():
        addr_to = raw_input('Enter valid e-mail address [to]: ')
        if re.search(r'[@]',addr_to):
            to=addr_to
        else:
            to=None
            print 'E-mail address not valid! Cannot send e-mail!'
        
        addr_cc = raw_input('Enter valid e-mail address [cc]: ')
        if re.search(r'[@]',addr_cc):
            cc=addr_cc
        else:
            cc=None
            print 'No [cc] given'
        return to,cc 

def download_proxy(url):
    b = mechanize.Browser()
    b.set_debug_http(True)
    b.set_handle_robots(False)
    b.addheaders=[mechanize_headers]
    
    print '\nDownloading http://proxyconf.srv.volvo.com/ ... \n'    
    try:
        r = b.open(url)
        content = r.read()
        with open(proxy,'w+') as f:
            f.write(content)
        print '\nProxy Updated! [%s] \n\n\n' % proxy
        time.sleep(2)
    except URLError, e:
        print 'Cannot download proxy PAC file!\n Program terminated...'
        sys.exit()
    

def run():
    #download http://proxyconf.srv.volvo.com/
    download_proxy(proxy_url)
    
    #get list of URLs to check redirects (from input_file)
    redirects_list = input_data(input_file)
    
    #create url_requests and save all the data to .content variable
    log_content = fetch_url(redirects_list)
    
    #when all the URLs are already opened/redirected and all the outputs are written to logger.content
    #lets generate graphic_log file
    parser = Output_Parser(log_content, graphic_log)
    out_dict = parser.generate_output()
    
    #Finally, lets check if all redirects are correct and generate final_log (LOG or XLS)
    parser.verify_redirects(redirects_list[1], out_dict, 'xls')
    
    

def main():
    print INTRO
    to, cc = get_email_addresses()
    
    ans = raw_input('START [y/n]? ')
    if ans == 'y':
        print 'Starting...\n'
        time.sleep(2)
        run()
        
        """
        sendmail with resutls to the recipients
        """
        if to and not cc:
            send_mail(To=to, Subject='Redirect_Tool has finished!'\
                  ,Body='Logs attached', Attachments=[graphic_log, detailed_log, xls_report])
        if to and cc:
            send_mail(To=to, Cc=cc, Subject='Redirect_Tool has finished!'\
                  ,Body='Logs attached', Attachments=[graphic_log, detailed_log, xls_report])
        
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
