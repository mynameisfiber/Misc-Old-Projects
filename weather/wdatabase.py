#!/usr/bin/env python
# Michael Gorelick, Jan 2009
# GNU/GPL

from os import path
import datetime  
import numpy as n

class wdatabase:
  def __init__(self,station,root=None):
    """Initialize database created by getweather.py.  Station is the station ID as given
    by climate.weatheroffice.ec.gc.ca and root is the database directory"""
    self.station = station
    if not root:
      self.root = "./"
    else:
      self.root = path.abspath(root)
    self.root = path.join(self.root,str(self.station))
    self.curday = None
    self.date = None
    self.fields = ['date', 'year', 'month', 'day', 'time', 'temp', '', \
   'dew point', '', 'humidity', '', 'wind dir', '', 'wind speed', '', \
   'visibility', '', 'pressure', '', 'hmdx', '', 'wind chill', '','weather']

  def getfilename(self,cur):
    return path.join(self.root,"%04d/%02d.cvs"%(cur.year,cur.month))

  def loadfile(self,cur):
    if self.curday and (self.curday.month,self.curday.year) == (cur.month,cur.year):
      return self.data
    self.curday = cur
    data = []
    try:
      fd = file(self.getfilename(cur))
    except IOError:
      raise Exception("Date is not in the database: %s"%cur)
    for lineno, line in enumerate(fd.xreadlines()):
      if lineno >= 16:
        data.append(dict([(self.fields[i], self.parse(x.strip('"'),i)) \
        for i,x in enumerate(line.strip().split('","')) if x.strip('"')]))
    self.data = data
    return data
    
  def parse(self,item,i):
    if 0 < i < 23 and i != 4:
      try:
        return float(item)
      except ValueError:
        pass
    return item

  def getIndex(self,day):
    return (day.day-1)*24 + day.hour 

  def getDateTime(self,day):
    """Returns an hours data for a given datetime.  Day must be a datetime object"""
    return self.loadfile(day)[self.getIndex(day)]
    
  def wrange(self,start,end,dt=datetime.timedelta(seconds=3600)):
    """Returns an iterator from start to end using step dt. start and end must
    be datetime objects while dt is a timedelta"""
    cur = start
    curday = datetime.datetime(1,1,1)
    while cur < end:
      yield self.getDateTime(cur)
      cur += dt
        
if __name__ == '__main__':
  from datetime import datetime as t, timedelta as dt
  d = wdatabase(5097,root="data")
  for x in d.wrange(t(1953,1,1),t(1954,1,1),dt(days=1)):
    print "%(date)15s: %(temp)6.2fC / %(weather)s"%x
