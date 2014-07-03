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

def get_special_paths(dir):
  filenames = os.listdir(dir)
  result = []
  for filename in filenames:
    match = re.search(r"__(\w*)__", filename)
    if match != None:
      result.append(os.path.abspath(filename))
  return result

def copy_to(paths, dir):
  if os.path.exists(dir) != True:
    os.mkdir(dir)
  for path in paths:
    shutil.copy(path, dir)
  return

# doesn't work on windows
def zip_to(paths, zippath):
  for path in paths:
    cmd = "7z a -t7z " + zippath + " " + path

    print "Command to run:", cmd
    (status, output) = commands.getstatusoutput('dir')
    if status:
      sys.stderr.write("Err: " + output)
      sys.exit(1)
    print output
  return
  
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
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  result = get_special_paths(args[0])
  if todir != '':
    copy_to(result, todir)
  if tozip != '':
    zip_to(result, tozip)
  print result
  
if __name__ == "__main__":
  main()
