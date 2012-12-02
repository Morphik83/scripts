from fetchURL_byProxy import *

redirects_list = ['http://volvopenta.com','http://volvopenta.com','http://volvopenta.com']
pacfile = 'C:\\tmp\\proxyconf_srv_volvo_com'
log = 'D:\\tmp\\Redirect_Handler.log'               #INFO log

"""
Below logger obj is used to overwrite standard 'write' method of the 'sys.stdout'
In general, 'print' statement by default executes 'write' method on 'sys.stdout' object - by overwritting
this method, it is possible to redirect all the data to eg. file or another obj (see Logger class for details)
"""
logger = loggers.Logger()   #creates DefaultLogM (DEBUG log) file - see in Logger obj for details
                            #redirect all the outputs to the logger obj
                            
try:
    for url in redirects_list:
        try:
            response = fetchurl(pacfile, url)   #by using 'fetchurl' we connect to network by PAC proxy file
            if response:
                pprint.pprint(response.__dict__)  #because sys.stdout is redirected, all the info is parallelly printed 
                print 40*'*'                        #on the output, written to logger.content object and written to the log file
            else:
                sys.stderr.write('URL %s could not be retrieved using PAC file %s.' %(url, pacfile))
        except Exception, e:
            print "There was a problem with opening URL. Error: ",e
except Exception,e:
    print "Problem with getting URL from url_list",e
finally:
    sys.stdout = sys.__stdout__                 #revert sys.stdout to normal