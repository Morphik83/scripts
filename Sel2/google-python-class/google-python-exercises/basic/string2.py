#!/usr/bin/python2.4 -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
from string import replace
import re

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Additional basic string exercises

# D. verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
    def funct_1(s):
        list = [x for x in s[len(s)-3:]]
        if list[0]== 'i' and list[1]=='n' and list[2]=='g':
            list.append('ly')
            #list.extend(['ing'])
            return str(s[:len(s)-3])+"".join(list)
        else:
            list.append('ing')
            return str(s[:len(s)-3])+"".join(list)
        
    def funct_2(s):
        return (str(s[len(s)-3:]) == 'ing') and (lambda x : x +'ly')(s) or (lambda x : x +'ing')(s)
            
    #return (lambda s : len(s))(s)>=3 and funct_1(s) or (lambda s : s)(s)
    return (lambda s : len(s))(s)>=3 and funct_2(s) or (lambda s : s)(s)


# E. not_bad
# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
# So 'This dinner is not that bad!' yields:
# This dinner is good!
def not_bad(s):
    
  searchTextPattern = re.compile(r'(\b(n|N)ot\b)\s+\w+\s+(\b(b|B)ad\b)\s*\w*')
  #\b-word boundary, (n|N) - n or N, \s+ -any whitespace (1 or more), \w+ - any alphanumeric
  #[a-zA-Z0-9]

  return re.sub(searchTextPattern, 'good', s)


# F. front_back
# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
def front_back(a, b):
    
    str_list = [a, b]
    new_list = []
    for S in str_list:
        if len(S)%2==0:
            #print len(S)
            #print S[:len(S)/2]+"_"+ S[len(S)/2:]
            new_list.append(S[:len(S)/2])
            new_list.append(S[len(S)/2:])
        elif len(S)%2!=0:
            #print len(S)
            #print S[:(len(S)/2)+1]+"_"+S[(len(S)/2)+1:]
            new_list.append(S[:(len(S)/2)+1])
            new_list.append(S[(len(S)/2)+1:])
        
    #print new_list
    #print "".join(new_list[0]+new_list[2]+new_list[1]+new_list[3])
    return "".join(new_list[0]+new_list[2]+new_list[1]+new_list[3])
     
def front_back_2(a,b):
    str_list = [a,b]
    new_list = []
    
    def f1(S):
        [new_list.append(x) for x in [S[:len(S)/2], S[len(S)/2:] ]]
    def f2(S):
        [new_list.append(x) for x in [S[:(len(S)/2)+1], S[(len(S)/2)+1:] ]]
    for S in str_list:
        (lambda s: len(s)%2==0)(S) and [f1(S)] or f2(S)
    #[f1(S)] - has to be list, because non-empty list is always true!
    
    return "".join(new_list[0]+new_list[2]+new_list[1]+new_list[3])


def xxx(number):
    phonePattern = re.compile(r'^(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d+)$')
    return bool(phonePattern.search(number))


def regularExpr(testStr):
    
    searchTextPattern = re.compile(r'(\b(n|N)ot\b)\s+\w+\s+(\b(b|B)ad\b)\s*\w*')
    print 'testStr: |' + testStr+'|'
    return bool(re.search(searchTextPattern, testStr))

# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
    print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))
    print
    return True

  else:
    prefix = '  X '
    print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))
    print
    return False
  

# main() calls the above functions with interesting inputs,
# using the above test() to check if the result is correct or not.
def main():
  test(xxx('80055590001234'),True)  
  print 'verbing'
  test(verbing('hail'), 'hailing')
  test(verbing('swiming'), 'swimingly')
  test(verbing('do'), 'do')

  print
  print 'not_bad'
  test(not_bad('This movie is not so bad'), 'This movie is good')
  test(not_bad('This dinner is not that bad!'), 'This dinner is good!')
  test(not_bad('This tea is not hot'), 'This tea is not hot')
  test(not_bad("It's bad yet not"), "It's bad yet not")

  print
  print 'front_back'
  test(front_back('abcd', 'xy'), 'abxcdy')
  test(front_back('abcde', 'xyz'), 'abcxydez')
  test(front_back('Kitten', 'Donut'), 'KitDontenut')\
  
  print
  print 'front_back_2'
  test(front_back_2('abcd', 'xy'), 'abxcdy')
  test(front_back_2('abcde', 'xyz'), 'abcxydez')
  test(front_back_2('Kitten', 'Donut'), 'KitDontenut')
  
  print
  print 'not .... bad'
  """
  test(regularExpr('aaanotaaa'), False)
  test(regularExpr('aaa not aaa'), False)
  test(regularExpr('not aaa'), False)
  test(regularExpr('notaaa'), False)
  test(regularExpr('aaanot'), False)
  test(regularExpr('aaa not'), False)
  test(regularExpr('Not aaa'), False)
  test(regularExpr('aaa Not'), False)
  test(regularExpr('aaaNOTaaa'), False)
  """
  #create dictionary {'string':True/False}
  
  #use kwarg to pass parameters to test(regularExpr(key),val)
  test(regularExpr('maciek not that bad'), True)
  test(regularExpr('maciek not that Bad'), True)
  test(regularExpr('maciek not that bad '), True)
  test(regularExpr('maciek not that bad some extra'), True)
  test(regularExpr('This dinner is not that bad!'), True)
  test(regularExpr('maciek notThat bad'), False)
  test(regularExpr('maciek not thatBad'), False)
  test(regularExpr('maciek not bad'), False)
  test(regularExpr('maciek notbad'), False)
  test(regularExpr('maciek notBad'), False)
  test(regularExpr('maciek badnot'), False)
  test(regularExpr('maciek badNot'), False)
  test(regularExpr('maciek bad not'), False)
  test(regularExpr('maciek bad that not'), False)
  
if __name__ == '__main__':
    main()
    
    #print new_list.append(['maciek'],['bartek'])
    #print [x for x in [S[:len(S)/2], S[len(S)/2:] ]]
    
    """
    str_list = ['maciek', 'bartek']
    new_list = []
    def f1(S):
        new_list.append(S[:len(S)/2])
        new_list.append(S[len(S)/2:])
    def f2(S):
        new_list.append(S[:(len(S)/2)+1])
        new_list.append(S[(len(S)/2)+1:])
    for S in str_list:
        (lambda s: len(s)%2==0)(S) and [f1(S)] or f2(S)
        print new_list
        
    print "".join(new_list[0]+new_list[2]+new_list[1]+new_list[3])
    
    #return "".join(new_list[0]+new_list[2]+new_list[1]+new_list[3])
    """
    """
    str_lis = ['maciekb', 'bartek']
    new_list = []
    for S in str_lis:
        if len(S)%2==0:
            print len(S)
            print S[:len(S)/2]+"_"+ S[len(S)/2:]
            new_list.append(S[:len(S)/2])
            new_list.append(S[len(S)/2:])
        elif len(S)%2!=0:
            print len(S)
            print S[:(len(S)/2)+1]+"_"+S[(len(S)/2)+1:]
            new_list.append(S[:(len(S)/2)+1])
            new_list.append(S[(len(S)/2)+1:])
        
    print new_list
    print "".join(new_list[0]+new_list[2]+new_list[1]+new_list[3])
    #return "".join(new_list[0]+new_list[2]+new_list[1]+new_list[3])
    """
        
        
  
    #searchTextPattern = re.compile(r'\bnot')
    #print re.search(searchTextPattern, testStr)
    #if len(s) >=3:
    #    newString = lambda s: s.split()+['ing']
    #    print "".join(newString(s))
    # 
    #print "________"
    #s1 = 'maciek not so bads'
    #s2 = 'not'
    #s3 = 'bad'
    
    #str_list = s1.split()
    #print str_list
    #if 'not' in s1 and 'bad' in s1:
    #    print 'ok'  
    """
    if s1.find(s3)> s1.find(s2):
        print 'bad follows not'
        
    else:
        print 'bad does not follow not'
    """    
    
    """  
    def f(s):
        print "length of test string is more than 3"
        return True
                          
    test_str = 'ma'
    lam =  (lambda x : len(x))(test_str) >= 3 and f(test_str) or (lambda x:x)(test_str)
 
    print lam
    """ 
    """
    s = 'hailing'
    a =  (str(s[len(s)-3:]) == 'ing') and (lambda x : x +'ly')(s) or (lambda x : x +'ing')(s)
    print a
    """
    
    #test_str = 'This movie is not so bad '
    #test_str = 'This dinner is not that bad!'
    test_str = 'This tea is not hot'
    #test_str = "It's bad yet not"
    
    import re
    YYYY_MM = 'mmaciek 1234-56 eee'
    #pattern = re.compile(r'\b(\d{4}-\d{2})\b')
    #print re.sub(r'\b(\d{4}-\d{2})\b', '9999-99', YYYY_MM)
    #print pattern.search(YYYY_MM)
    
    
    #pattern = re.compile(r'\b(\d{4}-\d{2})\b')
    #a = pattern.search(YYYY_MM)
    #print a
    
    
   