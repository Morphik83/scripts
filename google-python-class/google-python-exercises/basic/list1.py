#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0


# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Basic list exercises
# Fill in the code for the functions below. main() is already set up
# to call the functions with a few different inputs,
# printing 'OK' when each function is correct.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code.
# It's ok if you do not complete all the functions, and there
# are some additional functions to try in list2.py.

# A. match_ends
# Given a list of strings, return the count of the number of
# strings where the string length is 2 or more and the first
# and last chars of the string are the same.
# Note: python does not have a ++ operator, but += works.
def match_ends_(words):
    
    new_list = []    
    for s in words:
        (lambda s: len(s)>=2)(s) and (lambda s: str(s[0])==str(s[-1]))(s) and new_list.append(s) 
    return len(new_list)


def match_ends(words):
    count = 0
    for word in words:
        if len(word)>=2 and word[0]==word[-1]:
            count = count +1
    return count
# B. front_x
# Given a list of strings, return a list with the strings
# in sorted order, except group all the strings that begin with 'x' first.
# e.g. ['mix', 'xyz', 'apple', 'xanadu', 'aardvark'] yields
# ['xanadu', 'xyz', 'aardvark', 'apple', 'mix']
# Hint: this can be done by making 2 lists and sorting each of them
# before combining them.
def front_x_1(words):
    x_list = []
    rest_list = []
    #create two lists: 
    for x in words:
        if x[0]=='x':
            x_list.append(x)
        else:
            rest_list.append(x)
    
    return sorted(x_list)+sorted(rest_list)

def front_x_2(words):
    x_list = [x for x in words if x[0]=='x']
    rest_list = [x for x in words if x not in x_list] 
    
    return sorted(x_list)+sorted(rest_list)
    
def front_x_3(words):
    
    return sorted([x for x in words if x[0]=='x'])+sorted([x for x in words if x not in [x for x in words if x[0]=='x']] )

def front_x_ (words):
    x_list = []
    rest_list = []
    for x in words:
        (lambda x : x[0]=='x')(x) and [x_list.append(x)] or rest_list.append(x)
    """
    why do we need to put [] around x_list.append(x) ?
    -print bool(x_list.append(x)) -> always returns FALSE, so eg.
    lets x='xxxx' > lambda x: x[0]=='x' RETURNS TRUE->x_list.append(x) executes
    but returns FALSE-> TRUE and FALSE returns FALSE-> FALSE or rest_list.append(x) (ALSO FALSE!)
    returns last FALSE, so rest_list.append(x)  is also executed.
    In that way x='xxxx' is appendd to two lists: x_list and rest_list.
    To avoid this, [] has to be used in x_list.append(x) - non-empty list is always TRUE.
    """
    return sorted(x_list)+sorted(rest_list)


def front_x(words):
    x_list = []
    rest_list = []
    for word in words:
        if word.startswith('x'):
            x_list.append(word)
        else: rest_list.append(word)
        
    return sorted(x_list)+sorted(rest_list)
            
    
    
    
    
# C. sort_last
# Given a list of non-empty tuples, return a list sorted in increasing
# order by the last element in each tuple.
# e.g. [(1, 7), (1, 3), (3, 4, 5), (2, 2)] yields
# [(2, 2), (1, 3), (3, 4, 5), (1, 7)]
# Hint: use a custom key= function to extract the last element form each tuple.
def sort_last_(tuples):
    return sorted(tuples, key = lambda par:par[-1])

from operator import itemgetter
def sort_last(tuples):
    return sorted(tuples, key = itemgetter(-1))


class Student:
    def __init__ (self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age
    def __repr__(self):
        return repr((self.name, self.grade, self.age))


# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))


# Calls the above functions with interesting inputs.
def main():
  print 'match_ends'
  test(match_ends(['aba', 'xyz', 'aa', 'x', 'bbb']), 3)
  test(match_ends(['', 'x', 'xy', 'xyx', 'xx']), 2)
  test(match_ends(['aaa', 'be', 'abc', 'hello']), 1)

  print
  print 'front_x'
  test(front_x(['bbb', 'ccc', 'axx', 'xzz', 'xaa']),
       ['xaa', 'xzz', 'axx', 'bbb', 'ccc'])
  test(front_x(['ccc', 'bbb', 'aaa', 'xcc', 'xaa']),
       ['xaa', 'xcc', 'aaa', 'bbb', 'ccc'])
  test(front_x(['mix', 'xyz', 'apple', 'xanadu', 'aardvark']),
       ['xanadu', 'xyz', 'aardvark', 'apple', 'mix'])

       
  print
  print 'sort_last'
  test(sort_last([(1, 3), (3, 2), (2, 1)]),
       [(2, 1), (3, 2), (1, 3)])
  test(sort_last([(2, 3), (1, 2), (3, 1)]),
       [(3, 1), (1, 2), (2, 3)])
  test(sort_last([(1, 7), (1, 3), (3, 4, 5), (2, 2)]),
       [(2, 2), (1, 3), (3, 4, 5), (1, 7)])

def test_sorting():
    from operator import itemgetter,attrgetter
    student_objects = [Student('john', 'A', 15),
                       Student('mark', 'B', 12),
                       Student('jack', 'B', 10)]
    print '1:'
    print sorted(student_objects, key = lambda student:student.age)
    print '2:'
    print sorted(student_objects, key = attrgetter('age'))

    student_tuples = [('john', 'A', 15),('mark', 'B', 12),('jack', 'B', 10)]
    print '3:'
    print sorted(student_tuples, key = itemgetter(2))
    
    #Also possible reversed sorting direction:
    print '4:'
    print sorted(student_objects, key = attrgetter('age'), reverse = True)
    
    #difference between sort and sorted:
    print """sort is a built-in method (can be used only with lists! list.sort()), 
    but it modifies list in-place and returns nothing (None) !!
    So, below print returns None!!"""
    print student_tuples.sort()
    print """ To actually print sorted list, it is needed to:"""
    student_tuples.sort()
    print student_tuples
    
    print "itemgetter:"
    from operator import itemgetter
    print itemgetter(1)('ABCDE')
    #prints 'B'
    print itemgetter(1,3,5)('ABCDEFR')
    print itemgetter(slice(4,None))('ABCDEFGH')
    #prints 'EFGH'

        
        
if __name__ == '__main__':
    #main()
    #test_sorting()
    
    print 'test lambda:' 
    test_list_1 = [x for x in range(10)]
    #test_list_2 = [range(10)]
    print test_list_1
    
    print [x for x in test_list_1 if bool(x%3)==True]
    print [x for x in test_list_1 if bool(x%3)==False]
    "because if x%2=0 it is False! Otherwise, TRUE"
    
    #print [x for x in test_list_1 if ]
    #x = 10
    #print (lambda z:10*z)(x)
    #below should print only [9]
    #print [x for x in test_list_1 if (lambda z:10*z)(x)==90]
    
    for x in range(10):
        print x," ",x%3," ",bool(x%3)
    
    
    