#!/usr/bin/env python3
import datetime
from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot
import numpy
import psycopg2


def main():
	db = psycopg2.connect(database='james')
	cur = db.cursor()
	cur.execute('SELECT latitude,longitude,total FROM scats WHERE time=%s',
			(datetime.datetime(2015,5,1,9,0),))
	data = cur.fetchall()
	x = numpy.array([[r[0] for r in data]])
	y = numpy.array([[r[1] for r in data]])
	t = numpy.array([[r[2] for r in data]])
	#m = Basemap(width=120000,height=90000, projection='lcc',
	#		resolution='h', lat_0=-32.2,lon_0=115.8)
	#m.drawcoastlines()
	#m.drawrivers()
	#m.drawmapboundary(fill_color='aqua')
	#m.fillcontinents(color='coral',lake_color='aqua')
	#m.scatter(x,y,latlon=True, c='red', s=1000.0)
	im = pyplot.imread('map.png')
	pyplot.imshow(im)
	pyplot.scatter(x,y)
	pyplot.show()

if __name__ == '__main__':
	main()
