from fetchURL_byProxy import *

redirects_list = ['http://volvopenta.com','http://volvopenta.com','http://volvopenta.com']
pacfile = 'C:\\tmp\\proxyconf_srv_volvo_com'
#url = 'http://volvopenta.com'
sys.stdout = open("C:\\tmp\\redirect.log", "a+")

for url in redirects_list:
    response = fetchurl(pacfile, url)
    if response:
        pprint.pprint(response.__dict__)
        print 40*'*'
    else:
        sys.stderr.write('URL %s could not be retrieved using PAC file %s.' %(url, pacfile))  
