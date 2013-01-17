
class RootClass(object):
    
    def _info(self, *args):
        msg = []
        for arg in args:
            msg.append(arg)
        print "*INFO*", ''.join(map(str,msg))
        
    def _warn(self, *args):
        msg = []
        for arg in args:
            msg.append(arg)
        print "*WARN*", ''.join(map(str,msg))
        
    def _fail(self, error):
        raise AssertionError(error)