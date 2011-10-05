#!/usr/bin/env python
# Michael Gorelick Jan 2009
# GNU/GPL

from datetime import timedelta, date
from urllib import urlretrieve, urlopen
from os import makedirs, path, remove
import sys, re

log = "lastget.log"
def parseSave(savedir,year,month):
  dir = "%s/%04d/"%(savedir,year)
  try:
    makedirs(dir)
  except OSError:
    pass
  return dir+"%02d.cvs"%(month)

def getStartDate(station):
  data = "".join(urlopen("http://www.climate.weatheroffice.ec.gc.ca/climateData/hourlydata_e.html?timeframe=1&StationID=%d"%station).readlines())
  result = re.search("updateDays\(document\.forms\.namedItem\('frmNewYear1'\),(?P<year>[0-9]*),(?P<month>[0-9]*),[0-9,]*\)",data).groupdict()
  return (int(result["year"]), int(result["month"]))


if len(sys.argv) == 1:
  station = 5097
  savedir = "./data/%d/"%station
elif len(sys.argv) == 2:
  station = int(sys.argv[1])
  savedir = "./data/%d/"%station
elif len(sys.argv) == 3:
  station = int(sys.argv[1])
  savedir = "%s/%s"%(sys.argv[2],station)
else:
  print "Usage: %s <station ID> [save directory]"%sys.argv[0]
  exit(-1)

URL="http://www.climate.weatheroffice.ec.gc.ca/climateData/bulkdata_e.html?timeframe=1&Prov=XX&StationID=%(station)s&Year=%(y)d&Month=%(m)d&format=csv&type=hly"
parseURL = lambda station,year,month : URL%{"y":year,"m":month,"station":station}

print "Finding out when data begins"
try:
  sy, sm = [int(x) for x in file("%s/log"%savedir).readlines()[0].split('-')]
except IOError:
  sy, sm = getStartDate(station)
enddate = date.today()

while True:
  print "Getting %04d-%02d\t\t"%(sy,sm),
  sys.stdout.flush()
  if path.isfile(parseSave(savedir,sy,sm)):
    remove(parseSave(savedir,sy,sm))
  urlretrieve(parseURL(station,sy,sm), parseSave(savedir,sy,sm))
  open("%s/log"%savedir,"w+").write("%04d-%02d"%(sy,sm))
  print "[DONE]"
  if sm == 12:
    sm = 1
    sy += 1
  else:
    sm += 1
  if sy > enddate.year or (sy == enddate.year and sm > enddate.month):
    break
