#!/usr/bin/env python3
import csv
import datetime
import psycopg2
import sys


def main():
	data = csv.reader(sys.stdin)
	db = psycopg2.connect(database='james')
	cur = db.cursor()
	for row in data:
		if 'WKT' == row[0]:
			# header
			continue
		tcsno = int(row[2])
		time = datetime.datetime.strptime(row[1], '%d/%m/%Y %H:%M')
		longitude = float(row[27])
		latitude = float(row[28])
		detectors = [int(c) for c in row[3:27] if c.isdigit()]
		total = sum(detectors)
		cur.execute('''INSERT INTO scats
			(tcsno, time, longitude, latitude, geom, detectors, total)
			VALUES (%s, %s, %s, %s, st_setsrid(st_makepoint(%s, %s), 4326), %s, %s)''',
			(tcsno, time, longitude, latitude, longitude, latitude, detectors, total))
	db.commit()


if __name__ == '__main__':
	main()
