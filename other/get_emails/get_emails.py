import os
import re
import urllib2

def get_mails():
    """Returns a list of email addresses extracted from page_source
    
    Input: page_source
    Output: get_mail.log with list of email addresses
    """
    #gets current working dir
    cwd = os.getcwd()
    
    #creates log_path/log files
    log_path = os.path.join(cwd, 'logs')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = os.path.join(log_path, 'get_mail.log')
    skipped_lines = os.path.join(log_path, 'skipped_lines.log')
    
    #page source
    page_source = os.path.join(cwd,'page_source')
    
    #compiles reqexp to extract emails
    re_pttrn = re.compile(r'mailto:(.*?@[\w\.]+\w+)',re.I)
     
    with open(log_file, 'w+') as log, open(skipped_lines,'w+') as skipped:
        try:
            with open(page_source, 'r+') as page:
                for line in page:
                    email_lst = re_pttrn.findall(line) 
                    if email_lst:
                        [(lambda email:log.write(email+'\n'))(email) for email in email_lst]
                    else:
                        skipped.write(line+'\n')
                             
                print 'DONE. \nCheck ',log_file
        except  IOError,e:
            print e

def get_mails_from_url(url):
    """Returns a list of email addresses extracted from page_source
    
    Input: page_source
    Output: get_mail.log with list of email addresses
    """
    #gets current working dir
    cwd = os.getcwd()
    
    #creates log_path/log files
    log_path = os.path.join(cwd, 'logs')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = os.path.join(log_path, 'get_mail.log')
    skipped_lines = os.path.join(log_path, 'skipped_lines.log')
    
    #page source
    page_source = urllib2.urlopen (url).read()
    
    #compiles reqexp to extract emails
    re_pttrn = re.compile(r'mailto:(.*?@[\w\.]+\w+)',re.I)
    
    with open(log_file, 'w+') as log, open(skipped_lines,'w+') as skipped:
        emails_lst = re_pttrn.findall(page_source) 
        if emails_lst:
            [(lambda email:log.write(email+'\n'))(email) for email in emails_lst]
    print 'DONE. \nCheck ',log_file
        
if __name__ == '__main__':
    #get_mails()
    
    url = 'http://dd710.com/email.htm'
    get_mails_from_url(url)
     
    