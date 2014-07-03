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
  f = open(filename, 'rU')
  result = []
  hostname = "http://" + filename.split('_')[1]
  dict = {}
  for line in f:
    # print line
    match = re.search(r"\"GET\s+([\w./~-]+puzzle[\w./~-]+)\s+HTTP/1.0\"", line)
    if match:
      if dict.get(match.group(1)) == None:
        result.append(hostname + match.group(1))
        dict[match.group(1)] = True
  result = sorted(result, key=decide_sort)
  f.close()
  return result

def decide_sort(str_value):
  match = re.search(r"\-\w+\-(\w+)\.jpg$", str_value)
  match2 = re.search(r"([\w.-]+)\.jpg$", str_value)
  if match:
    return match.group(1)
  elif match2:
    return match2.group(1)
  else:
    return str_value
  
def image_get(url, filename):
  print "Retrieve..."
  try:
    urllib.urlretrieve(url, filename)
  except IOError:
    print 'problem reading url:', url

def create_index(img_count, dest_dir):
    file = open("%s\\index.html" % (dest_dir), "w")

    file.write("<verbatim>")
    file.write("<html>")
    file.write("<body>")
    for count in range(1, img_count):
      file.write("<img src=\"img%d.jpg\">" % (count));
    file.write("</body>")
    file.write("</html>")
    file.close()
    
def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  if os.path.exists(dest_dir) == False:
    os.mkdir(dest_dir)
  img_count = 1
  for img_url in img_urls:
    image_get(img_url, "%s\\img%d.jpg" % (dest_dir, img_count))
    img_count += 1
  create_index(img_count, dest_dir)
    

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
    # create_index(3, todir)
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
