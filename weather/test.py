#!/usr/bin/env python

from wdatabase import wdatabase
from datetime import datetime,timedelta
import sys

print "Getting Data"
d = wdatabase(5097,"data")
data = []
for info in d.wrange(datetime(1953,1,5,12,0),datetime(2000,1,1),timedelta(days=365)):
  print "\r" + info["date"] + " "*10,
  sys.stdout.flush()
  try:
    data.append(info["temp"])
  except KeyError,e:
    pass
print "Graphing"
import pylab as py

py.plot(data)
py.show()
