
class RootClass:
    
    def _info(self, msg):
        print "*INFO*", msg
        
    def _warn(self, msg):
        print "*WARN*", msg
    
    def _fail(self, error):
        raise AssertionError (error)
        