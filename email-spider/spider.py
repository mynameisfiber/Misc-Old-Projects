#!/usr/bin/python
#
# Copyright 2008 Michael Gorelick 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see:
# http://www.gnu.org/licenses/gpl.html.

import Queue, re, urllib2, sys
import formatter, htmllib, urlparse
from cStringIO import StringIO

class Spider:
  def __init__(self, site, linkQueue, linkFinished, emailfile="emails.txt"):
    self.site = site
    self.domain = urlparse.urlparse(site).hostname
    self.emailfile = emailfile
    
    self.linkQueue = linkQueue
    self.linkFinished = linkFinished
    
    self._f = formatter.AbstractFormatter(formatter.DumbWriter(StringIO()))
    
    self.linkQueue.put(site)
    
  def run(self):
    reLinks = re.compile(r"""href=['"]?([^ ]+?)['"]?""")
    reMail = re.compile(r"""href=['"]?mailto:([^ ])""")
    emails = []
    print "Starting"
    while not self.linkQueue.empty():
      curLink = self.linkQueue.get()
      if curLink in self.linkFinished:
        continue
      print "Doing %s"%curLink
      
      try:
        data = urllib2.urlopen(curLink).read()
      except urllib2.URLError:
        print "Could not find %s"%curLink
        continue
      
      #First get the links:
      try:
        links = self.getLinks(data)
      except Exception:
        continue
      
      #Now sort through them:
      for i, link in enumerate(links):
        if link.startswith("javascript:"):
          links.pop(i)
        elif (link.startswith("mailto:") or reMail.match(link) != None) and link[7:].strip() != "":
          emails.append((links.pop(i)[7:].strip(), curLink))
          file(self.emailfile, "a+").write("%s \t\t\t %s\n"%(emails[-1]))
          print "\tFound email: %s" % link[7:]
        else:
          tmp = urlparse.urldefrag(urlparse.urljoin( "http://%s/"%self.domain , link, False))[0]
          if urlparse.urlparse(tmp).hostname == self.domain and tmp not in self.linkFinished:
            self.linkQueue.put(tmp)
            
        self.linkFinished.append(curLink)     
        #lately, check through the source:
        # DO LATER!
    return emails
          
    
  def getLinks(self, html):
    htmlparser = htmllib.HTMLParser(self._f)
    htmlparser.feed(html)
    htmlparser.close()
    return htmlparser.anchorlist
    
if __name__ == "__main__":
  linkQueue = Queue.Queue()
  try:
    test = Spider(sys.argv[1], linkQueue, [])
  except IndexError:
    print "Email Spider by Michael Gorelick"
    print "Usage: %s [URL]" % sys.argv[0]
    exit(-1)
  print test.run()
    
