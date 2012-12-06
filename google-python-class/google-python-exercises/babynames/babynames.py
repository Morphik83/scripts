#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import os
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # +++your code here+++
  final_name = []
  ####### open and read file
  #print filename
  f = open(os.path.abspath(filename), 'rU')
  #read whole file at once - not good when file is bigger than memory size ;)
  myFile = f.read()
  #for line in f:
  #  print line.readline()
  #or print f.read()

  ####### find&print YEAR using regexp
  year_match = re.findall(r'(\d{4})(</h\d>)',myFile)
  if not year_match:
    sys.stderr.write('Couldn\'t find the year!\n')
    sys.exit(1)
  #return year_match[0][0]
  final_name.append(year_match[0][0])

  ####### find&print RANK/NAME1/NAME2
  #f = open(os.path.abspath(filename), 'r')
  rankAndNames = re.findall(r'<td>(\d{1,4})</td><td>(\w+)</td><td>(\w+)</td>',myFile)
  #for x in rankAndNames :
  #	print x
  """
  rankAndNames = [('1', 'Michael', 'Jessica'),('2', 'Christopher', 'Ashley'),...]
  """

  ###### add NAMEs and RANKS to dict - > {NAME1:RANK,NAME2:RANK, ...}
  ###### use NAMES as keys, RANK as values - since there are always two names
  ###### with the same RANK (to avoid RANK overwriting)
  test_dict ={}
  for x in rankAndNames :
    test_dict [x[1]]=x[0]
    test_dict [x[2]]=x[0]
          
  ##### to display sorted names:
  for key in sorted(test_dict):
    final_name.append(key + " " + test_dict [key])


  return final_name

def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  #extract_names(args[0])
  
  for arg in args[0:]:
    text = '\n'.join(extract_names(arg))
  
    if summary:
        summaryFile = open(os.path.abspath(arg+'.summary'), 'w')
        summaryFile.write(text)
        summaryFile.close()
    else:
       print text
        
  


  
      
if __name__ == '__main__':
  main()
  #print "\n".join(extract_names("baby1990.html"))













