#!/usr/bin/python

from wdatabase import wdatabase
import datetime

print "Getting data"

d = wdatabase(5097,"data")
#d = wdatabase(30247,"data")
end = datetime.datetime.now()
start = end - datetime.timedelta(days=4)
dt = datetime.timedelta(hours=1)

print "Finding from %s to %s"%(start,end)
data = []
for item in d.wrange(start,end,dt):
  try:
    data.append( item["pressure"] )
  except KeyError:
    data.append( data[-1] )

print "Plotting"
import pylab
import matplotlib
import matplotlib.dates

fig = pylab.figure()
ax = fig.gca()

ax.plot_date(pylab.drange(start,end,dt),data,"b.-")
pylab.xlabel("Date")
pylab.ylabel("Pressure")
pylab.title("Pressure vs Date")

ax.xaxis.set_major_locator(matplotlib.dates.HourLocator(byhour=[12]))
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M\n%d/%m/%y'))

fig.savefig("pressure-test.png")
fig.show()

