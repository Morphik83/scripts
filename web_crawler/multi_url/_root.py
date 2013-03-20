from time import strftime

class RootClass(object):
    
    def _info(self, *args):
        msg = []
        for arg in args:
            msg.append(arg)
        print '>>'+strftime("%H:%M:%S")+'<<'+' *INFO* '+''.join(map(str,msg))
        
    def _warn(self, *args):
        msg = []
        for arg in args:
            msg.append(arg)
        print '>>'+strftime("%H:%M:%S")+'<<'+' *WARN* '+''.join(map(str,msg))
        
    def _fail(self, error):
        raise AssertionError(error)