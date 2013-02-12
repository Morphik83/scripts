import mechanize

username = '****'
passwd = '*****'

def test():
    headers = ('User-Agent','Mozilla/4.0')
    url = 'http://www.address.com'
    
    browser = mechanize.Browser()
    browser.set_debug_http(True)
    browser.set_handle_robots(False)
    browser.set_debug_redirects(True)
    browser.set_debug_responses(True)
    browser.addheaders=[headers]

    response = browser.open(url)
    for form in browser.forms():
        print "Form name:", form.name
        print form
    
    browser.select_form(nr=0)
    browser["ctl00$BodyContent$login$UserName"]=username
    browser["ctl00$BodyContent$login$Password"]=passwd
    browser.submit(name='ctl00$BodyContent$login$LoginButton')
    for link in browser.links():
        print link
    
if __name__ == '__main__':
    test()