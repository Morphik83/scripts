


class Time:
    def __init__(self, h=0, m=0, s=0):
        assert 0<=h<=23
        assert 0<=m<=59
        assert 0<=s<=60
        
        self._hours = int(h)
        self._minutes = int(m)
        self._seconds = int(s)
        
    def hours(self):
        return self._hours
    def minutes(self):
        return self._minutes
    def seconds(self):
        return self._seconds
    def __repr__(self):
        return "{0:02d}:{1:02d}:{2:02d}".format(self.hours(), self.minutes(), self.seconds())

import re

class ZIPCode:
    #US Only
    def __init__(self, zip):
        self._zip = zip
        self.checkRep()
        
    def zip(self):
        return self._zip
    
    def checkRep(self):
        assert len(self.zip()) == 5
        for i in range(0,len(self.zip())):
            #assert '0' <= self.zip()[i] <= '9'   
            #assert  re.search(r'[0-9]{5}', self._zip) is not None 
            assert  re.search(r'\d{5}', self._zip) is not None
    
    
if __name__ == '__main__':
    #===========================================================================
    # t = Time(3.14, 0, 0)
    # print t
    # assert repr(t) == "03:00:00"
    #===========================================================================
    t = ZIPCode('12345')

    