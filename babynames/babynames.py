#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os

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

def extract_year(text):
  match = re.search(r"(Popularity\s*in\s*)(\d*)", text)
  
  return match.group(2)
  
def extract_tuples(text):
  tuples = re.findall(r"<tr align=\"right\"><td>\s*?(\d+)\s*?</td>\s*?<td>\s*?(\w*)\s*?</td>\s*?<td>\s*?(\w*)\s*?</td>", text)
  
  return tuples

def construct_dict(tuples):
  dict = {}
  for tuple in tuples:
    if dict.get(tuple[1]) == None:
      dict[tuple[1]] = int(tuple[0])
    elif dict.get(tuple[1]) > int(tuple[0]):
      dict[tuple[1]] = int(tuple[0])
    if dict.get(tuple[2]) == None:
      dict[tuple[2]] = int(tuple[0])
    elif dict.get(tuple[2]) > int(tuple[0]):
      dict[tuple[2]] = int(tuple[0])
  return dict

def sort_names(tuples):
  return sorted(tuples, key=last_of)

def last_of(tuple):
  return tuple[0]

def make_list(year, dict):
  list = [year]
  tuples = sort_names(dict.items())
  for tuple in tuples:
    list.append("%s %s" % tuple)
  return list
  
def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  f = open(filename, 'rU')
  text = f.read()
  f.close();
  
  year = extract_year(text)
  # print "Year: %s" % (year)
  tuples = extract_tuples(text)
  # print "Names: %s" % (tuples)
  dict = construct_dict(tuples)
  # print "Dict: %s" % (dict)
  rank_list = make_list(year, dict)
  # print "Dict: %s" % (rank_list)
  
  return rank_list


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

  if summary == False:
    file = open("mybabynameresults.txt", "w")
    for filename in args:
      list = extract_names(filename)
      text = '\n'.join(list) + '\n'
      file.write(text)
    file.close()
  else:
    filenames = os.listdir(".")
    for fname in filenames:
      match = re.search(r"" + args[0].replace(".","\.").replace("*",".*"), fname)
      if(match != None):
        filename = match.group()
        file = open("%s.summary" % filename, "w")
        list = extract_names(filename)
        text = '\n'.join(list) + '\n'
        file.write(text)
        file.close()
  
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  
if __name__ == '__main__':
  main()
