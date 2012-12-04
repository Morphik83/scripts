#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0


# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""Mimic pyquick exercise -- optional extra exercise.
Google's Python Class

Read in the file specified on the command line.
Do a simple split() on whitespace to obtain all the words in the file.
Rather than read the file line by line, it's easier to read
it into one giant string and split it once.

Build a "mimic" dict that maps each word that appears in the file
to a list of all the words that immediately follow that word in the file.
The list of words can be be in any order and should include
duplicates. So for example the key "and" might have the list
["then", "best", "then", "after", ...] listing
all the words which came after "and" in the text.
We'll say that the empty string is what comes before
the first word in the file.

With the mimic dict, it's fairly easy to emit random
text that mimics the original. Print a word, then look
up what words might come next and pick one at random as
the next work.
Use the empty string as the first word to prime things.
If we ever get stuck with a word that is not in the dict,
go back to the empty string to keep things moving.

Note: the standard python module 'random' includes a
random.choice(list) method which picks a random element
from a non-empty list.

For fun, feed your program to itself as input.
Could work on getting it to put in linebreaks around 70
columns, so the output looks better.

"""
import os
import random
import sys


COUNTER = 200
FINAL_TEXT = []

def create_file(path,filename):
  abs_path = os.path.abspath(path)
  if os.path.exists(abs_path):
    filename = abs_path+"\\"+filename
    f = open(filename, 'w')
    f.write("1.Functional testing of the new features mainly exploratory testing\
    2.Regression testing testing backward compatibility, eliminating possible problems caused by newly\
     implemented fixes or new features 3.SystemAcceptance Testing (11111 on User Requirements\
     4.Performance Testing (2222 on logs) 5.Writing/updating all kinds of test documentation\
     6.Test Automation Robot Framework & Selenium mainly 7.Bug fixes verification")
    f.close()
  
  mimic_dict(filename)  
  #return filename

def mimic_dict(filename):
  """Returns mimic dict mapping each word to list of words which follow it."""
  # +++your code here+++
  
  test_dict = {}
  f = open(filename, 'rU') 
  FILE = (f.read()).split()
  f.close()
  #print FILE
  test_dict[" "]=[FILE[0]]

  tmp_list = []
  #test_list = ['1','2','3','4','5','2','6','7','2','10','4','four','2','DWA']
  
  for x in range(0,len(FILE)):
    tmp_list =[]
    #print "x: ",x, "FILE[x]:",FILE[x]
    try:
      if test_dict.has_key(FILE[x]) is False:
        #print "debug1: ", tmp_list
        tmp_list.append(FILE[x+1])
        #print "debug2: ", tmp_list
        for i in range(x+1,len(FILE)):
          if FILE[i]== FILE[x]:
            tmp_list.append(FILE[i+1])
            #print "debug3: ",tmp_list
        test_dict[FILE[x]]=tmp_list
        #print "###################"
      #else:
       # print "%s is in dict - skip to next X\n" %FILE[x]
    except IndexError:
      print "List index out of range"
      
    
  out_file = open('output_file','w+')  
  for i in test_dict.items():   
    out_file.write(str(i)+"\n")
  out_file.close()
  
  return test_dict
 



def print_mimic(mim_dict, word):
  """Given mimic dict and start word, prints 200 random words."""
  # +++your code here+++
  global COUNTER
  
  while COUNTER > 0:
    print "COUNTER: ",COUNTER
  
    if mim_dict.has_key(word) is True:
      another_word = random.choice(mim_dict[word])
      FINAL_TEXT.append(another_word)
      print "OK: ",word
      print "OK-appended: ",another_word
      COUNTER = COUNTER - 1
      print "OK COUNTER -1: ",COUNTER,"\n\n"
      word = another_word
      #print_mimic(mim_dict, another_word)
    else:
      #if NO, use first word in dict
      word = mim_dict[" "][0]
      another_word = random.choice(mim_dict[word])
      FINAL_TEXT.append(another_word)
      COUNTER = COUNTER - 1
      print "NOK: ",word
      print "NOK-appended: ",another_word
      COUNTER = COUNTER - 1
      print "NOK COUNTER -1: ",COUNTER,"\n\n"
      #print_mimic(mim_dict, another_word)  
      word = another_word
      
  out_file = open('FINAL_TEXT_output_file','w+')  
  out_file.write(" ".join(FINAL_TEXT))
  out_file.close()
  
  print " ".join(FINAL_TEXT)  
  
    
def test():
  global COUNTER
  
  print COUNTER
  #temp_COUNTER = COUNTER-1
  COUNTER = COUNTER - 1
  print COUNTER
  
  #=============================================================================
  # while COUNTER >= 0:
  #  print "mm"
  #  COUNTER = COUNTER -1 
  # 
  #=============================================================================

  


# Provided main(), calls mimic_dict() and mimic()
def main():
  if len(sys.argv) != 2:
    print 'usage: ./mimic.py file-to-read'
    sys.exit(1)

  dict = mimic_dict(sys.argv[1])
  print_mimic(dict, '')


def split_by_length(s, block_size):
  w = []
  n = len(s)
  for i in range(0,n,block_size):
    print "\ni->",i
    print "i+block_size->",i+block_size
    w.append(s[i:i+block_size])
  return w


def return_next_word(word, list_of_words):
  try:
    index = list_of_words.index(word)
    return list_of_words[index+1]
  except IndexError:
    print 'List index our of range'  
    
if __name__ == '__main__':
  main()
  #create_file('c://', 'test_file')
  #mimic_dict('alice.txt')
  #print_mimic(mimic_dict('alice.txt'), "pardonedsss.'")
  
   #=============================================================================
   # test_dict = {}
   # test_list = ['1','2','3','4','5','2','6','7','2','10','4','four','2','DWA']
   # 
   # for x in range(0,len(test_list)):
   #  tmp_list =[]
   #  print "x: ",x, "test_list[x]:",test_list[x]
   #  try:
   #    if test_dict.has_key(test_list[x]) is False:
   #      print "debug1: ", tmp_list
   #      tmp_list.append(test_list[x+1])
   #      print "debug2: ", tmp_list
   #      for i in range(x+1,len(test_list)):
   #        if test_list[i]== test_list[x]:
   #          tmp_list.append(test_list[i+1])
   #          print "debug3: ",tmp_list
   #      test_dict[test_list[x]]=tmp_list
   #      print "###################"
   #    else:
   #      print "%s is in dict - skip to next X\n" %test_list[x]
   #  except IndexError:
   #    print "List index out of range"
   #    
   #  
   #  
   # print test_dict
   #=============================================================================
  
  
    
  
      
  
  
  
