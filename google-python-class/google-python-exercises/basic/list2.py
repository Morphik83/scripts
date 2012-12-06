#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0


# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Additional basic list exercises

# D. Given a list of numbers, return a list where
# all adjacent == elements have been reduced to a single element,
# so [1, 2, 2, 3] returns [1, 2, 3]. You may create a new list or
# modify the passed in list.
def remove_adjacent_(nums):
    for x in nums:
        if nums.count(x)==1:
            pass
        else:
            nums.remove(x)
    return nums

def remove_adjacent(nums):
    for x in nums:
        (lambda x: nums.count(x)!=1)(x) and nums.remove(x)
    return nums
    
def remove_adjacent_solution(nums):
    results = []
    for num in nums:
        if len(results)==0 or num != results[-1]:
            results.append(num)
    

# E. Given two lists sorted in increasing order, create and return a merged
# list of all the elements in sorted order. You may modify the passed in lists.
# Ideally, the solution should work in "linear" time, making a single
# pass of both lists.
def linear_merge_(list1, list2):
    return sorted(list1 + list2)

def linear_merge(list1, list2):
    results = []
    while len(list1) and len(list2):
        if list1[0] < list2[0]:
            results.append(list1.pop(0))
        else:
            results.append(list2.pop(0))
    results.extend(list1)
    results.extend(list2)
    
    return results
                
# Note: the solution above is kind of cute, but unfortunately list.pop(0)
# is not constant time with the standard python list implementation, so
# the above is not strictly linear time.
# An alternate approach uses pop(-1) to remove the endmost elements
# from each list, building a solution list which is backwards.
# Then use reversed() to put the result back in the correct order. That
# solution works in linear time, but is more ugly.


# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))
  
def else_while_test(t,s):
    """
    the 'else' statement in a loop is a bit weird at first. The content of the else clause is 
    executed only when the loop completes without a break statement.
    """
    while t < s:
        t += 1
        if t == 10: break
        print t
    else:
        print "s is < 10"
    
    
def test_breakAnd_Continue():
    t = 0 
    print 'continue statement: This prevents printing of 2 and 3'
    """
    continue statement is used to bypass the rest of the code in a loop early
    """
    while t < 10:
        t += 1
        if t == 2 or t == 3: continue
        print t
        
    print "break statement: This loop stops when t is 5"
    """
    break statement is used to exit the loop early
    """
    
    while t < 10:
        t += 1
        if t == 5: break
        print t 
    print 'loop done'
    
def zip_to_loop_overMultipleItems():
    a = ('a','b','c')
    b = [11,22,33]
    c = range(5)

    print zip(a,b,c) 
    print "OUTPUT: [('a', 11, 0), ('b', 22, 1), ('c', 33, 2)]"
    
    
    

# Calls the above functions with interesting inputs.
def main():
  print 'remove_adjacent'
  test(remove_adjacent([1, 2, 2, 3]), [1, 2, 3])
  test(remove_adjacent([2, 2, 3, 3, 3]), [2, 3])
  test(remove_adjacent([]), [])

  print
  print 'linear_merge'
  test(linear_merge(['aa', 'xx', 'zz'], ['bb', 'cc']),
       ['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge(['aa', 'xx'], ['bb', 'cc', 'zz']),
       ['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge(['aa', 'aa'], ['aa', 'bb', 'bb']),
       ['aa', 'aa', 'aa', 'bb', 'bb'])


if __name__ == '__main__':
    #main()
    #list_1 = ['aa', 'xx']
    #list_2 = ['bb', 'cc', 'zz']
   zip_to_loop_overMultipleItems()
    
    #print sorted(list_1 + list_2)

    
    
    
    
    
    
    
    
    
    
    
    