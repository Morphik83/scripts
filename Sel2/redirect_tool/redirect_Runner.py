from fetchURL_byProxy import fetchurl,isproxyalive
from output_parser import Output_Parser


#Two log files are created:
#    1. Detailed Info - Default_Redirect.log (in redirect_tool dir)
#    2. Graphical Log - defined by 'log', general redirect info

#===============================================================================
# TODO: 
# -read URLs from txt file
# -add assertions (unti tests?)
# -(url_1 -> url_2) (but: url_1 ---> url_2 ---> url_3)| check that url_2 == urls[1]
#===============================================================================


redirects_list = ['http://volvopenta.com','http://volvobuses.com','http://volvo.com','http://volvotrucks.com']
pacfile = 'C:\\tmp\\proxyconf_srv_volvo_com'        #PAC proxy file
log = 'D:\\tmp\\Redirect_Handler.log'               #INFO log: log file, when redirects will be displayed in graphical way



"""
logger obj is used to overwrite standard 'write' method of the 'sys.stdout'
In general, 'print' statement by default runs 'write' method on 'sys.stdout' object - by overwritting
this method, it is possible to redirect all the data to eg. file or another obj (see Logger class for details)
"""
logger = loggers.Logger()   #creates DefaultLog (DEBUG log) file - see in Logger obj for details
sys.stdout = logger         #redirect all the outputs to the logger obj
                            
                            
"""
by using 'fetchurl' we connect to network by PAC proxy file
setting http_debuglevel=1 in fetchurl causes all the detailed info to be displayed on sys.stdout 
(but we redirected that strem to 'logger', so all the data is being saved in logger.content as well) 
"""                            
try:
    for url in redirects_list:
        try:
            fetchurl(pacfile, url)   
        except Exception, e:
            print "There was a problem with opening URL. Error: ",e
 
    """
    when all the URLs are already opened/redirected and all the outputs are written to logger.content
    lets generate final log file (log)
    """   
    parser = Output_Parser(logger.content, log)
    parser.generate_output()

finally:
    sys.stdout = sys.__stdout__                 #revert sys.stdout to normal