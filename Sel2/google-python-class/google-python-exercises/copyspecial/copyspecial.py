#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them


#gather a list of the absolute paths of the special files
#special = means the ones that have (__w__) underscore somewhere in the name

def getAbsPath(dir):
  filenames = os.listdir(dir)
  special_file_list =[]
  regular_file_list =[]
  for filename in filenames:
    special_file = re.search(r'([_]+)([a-zA-Z0-9]+)([_]+)',filename)

    if special_file:
      path = os.path.join(dir, filename)
      #print os.path.abspath (path)
      #print special_file.group(),'\n'
      special_file_list.append(os.path.abspath (path))
    else:
      #print 'regular filename: ',filename
      regular_file_list.append(filename)

  return [special_file_list,regular_file_list]


def copyFiles(src_folder ,destination_folder):
  files_to_copy =  getAbsPath (src_folder)[0]
  for file in files_to_copy:
    shutil.copy(file,os.path.abspath(destination_folder))


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[1] == '--todir':
    todir = args[2]
    del args[2:]
    #args[0] - source file, args[1] - destination folder
    copyFiles(args[0],todir)

  tozip = ''
  if args[1] == '--tozip':
    tozip = args[2]
    del args[2:]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions

  print "\n".join(getAbsPath (args[0])[0])
  
if __name__ == "__main__":
  main()
  #getAbsPath('.')
