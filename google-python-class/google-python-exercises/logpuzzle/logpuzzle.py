#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  test_list = []
  animal = False
  place = False
  
  if (re.search(r'(^.*)(_)(.*$)',filename)).group(1) == 'animal':
    animal = True
  elif (re.search(r'(^.*)(_)(.*$)',filename)).group(1) == 'place':
    place = True
  else:
    sys.stderr.write("Provide valid file name! <animal_code.google.com or place_code.google.com>")
    sys.exit(1)
  
  f = open( os.path.abspath(filename),'rU')
  matches = re.findall(r'(GET\s)(/edu/languages/google-python-class/images/puzzle/.*)(\sHTTP)', f.read())
  #=============================================================================
  #print len(matches)
  #print matches
  #=============================================================================
  if not matches:
      sys.stderr.write("RegExp did not find any match!")
      sys.exit(1)
      
  for match in matches:
      if match[1] not in test_list:
        test_list.append(match[1])
      
  if animal:
    test_list.sort(reverse=True)
    test_list = [ "http://%s%s" % ((re.search(r'(_)(.*$)',filename)).group(2),x) for x in test_list]     
    
  if place:
    #in sort, lambda gets following place_list elements (x), and operates on them
    #eg.URL = code.google.com/edu/languages/google-python-class/images/puzzle/p-bdfh-baad.jpg
    #sort by second word, .*/p-word-word.jpg
    #reg exp - match any [a-z] four letters, but only if followed by string ".jpg"
    test_list.sort(key = (lambda x: (re.search(r'([a-z]{4}(?=\.jpg))',x)).group()), reverse=True)
    #gets address from filename, eg/ animal_code.google.com
    test_list = [ "http://%s%s" % ((re.search(r'(_)(.*$)',filename)).group(2),x) for x in test_list]
    #print "\n".join(place_list)
  
  return test_list

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  abs_path = os.path.abspath(dest_dir)
  if not os.path.exists(abs_path):
    os.mkdir(abs_path)
    
  i = len(img_urls)
  for url in img_urls:
    print 'Retrieving img%s'%i
    urllib.urlretrieve(url, abs_path+"\\"+"img%s"%i)
    #print url
    i=i-1
    
  create_image_html(abs_path, len(img_urls))
  
def create_image_html(dir, counter):
  print '\nCreating index.html...'
  f = open(dir+'\\'+'index.html','w+')
  f.write('<verbatim>')
  for i in range(1,counter+1):
      print '<img src="img%s">'%i
      f.write('<img src="img%s">\n'%i)
  f.write('</verbatim>')
  f.close()
  
  #=============================================================================
  # opens index.html in default browser
  #=============================================================================
  os.startfile(dir+'\\'+'index.html')  
  

def main():
  
  args = sys.argv[1:]
  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]
    
  img_urls = read_urls(args[0])
  
  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

  

if __name__ == '__main__':
  main()
  #read_urls('place_code.google.com')
  
  #=============================================================================
  # f = open('d:/mac_iek/index.html','w+')
  # f.write('<verbatim>')
  # for i in range(1,201):
  #    f.write('<img src="img%s">\n'%i)
  # f.write('</verbatim>')
  # f.close()
  #=============================================================================
  #=============================================================================
  #=============================================================================
  # import urllib
  # 
  # f = urllib.urlopen('http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baaa.jpg')
  # urllib.urlretrieve('http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baaa.jpg', 'd:/maciek/img')
  # 
  #=============================================================================
  
