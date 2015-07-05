#!/usr/bin/env python3
import datetime
from flask import Flask
import json
import os
import psycopg2

app = Flask(__name__)
db = psycopg2.connect(database='james')

pie_tcsno = 14
pie_time = datetime.datetime(2015,5,1,7,0)

@app.route("/")
def main_page():
	# possibly not the best way to do this...
	return open("map.html").read()

@app.route("/locations")
def get_locations():
	cur = db.cursor()
	cur.execute("SELECT tcsno, latitude, longitude FROM scats_locations")
	data = cur.fetchall()
	db.commit()
	return json.dumps(data)


def get_next_time(time):
	cur = db.cursor()
	cur.execute("SELECT time FROM scats_times WHERE time>%s ORDER BY time LIMIT 1",
			(time,))
	res = cur.fetchone()
	if not res:
		return None
	return res[0]


@app.route("/data/<time>")
def get_data_at_time(time):
	global pie_time
	time_fmt = '%Y%m%d%H%M'
	time = datetime.datetime.strptime(time, time_fmt)
	pie_time = time
	next = get_next_time(time)
	if next:
		next = next.strftime(time_fmt)
	else:
		next = ''
	cur = db.cursor()
	cur.execute('SELECT tcsno, total FROM scats WHERE time=%s', (time,))
	data = cur.fetchall()
	db.commit()
	return json.dumps({'data': data, 'next': next,
			'time': time.strftime('%Y/%m/%d %H:%M')})


@app.route("/tcsdata/<tcsno>")
def get_tcs_data(tcsno):
	cur = db.cursor()
	cur.execute("SELECT to_char(time,'YYYY/MM/DD HH24:MI'), total"
			" FROM scats WHERE tcsno=%s", (tcsno,))
	data = cur.fetchall()
	db.commit()
	return json.dumps(data)

@app.route("/tcs/<tcsno>")
def get_tcs_info(tcsno):
	global pie_tcsno
	pie_tcsno = tcsno
	res = {'tcsno':tcsno}
	imgpath =  'static/maps/TCS {} Map.png'.format(int(tcsno))
	if os.path.isfile(imgpath):
		res['img'] = imgpath
	return json.dumps(res)


@app.route("/pie")
def get_pie():
	res = {}
	res['tcsno'] = pie_tcsno
	res['time'] = pie_time.strftime('%Y%m%d%H%M')
	return json.dumps(res)


@app.route("/piedata/<tcsno>/<time>")
def get_pie_data(tcsno, time):
	time_fmt = '%Y%m%d%H%M'
	t1 = datetime.datetime.strptime(time, time_fmt)
	t2 = t1 + datetime.timedelta(days=1)
	cur = db.cursor()
	cur.execute("SELECT time, detectors FROM scats"
			" WHERE tcsno=%s AND time>=%s AND time<%s"
			" ORDER BY time", (tcsno, t1, t2))
	res = []
	for t, dets in cur.fetchall():
		fake_detectors = [0,0,0,0]
		for i, count in enumerate(dets):
			fake_detectors[i%4] += count
		res.append({'time': t.strftime(time_fmt), 'detectors':fake_detectors})
	db.commit()
	return json.dumps(res)


if __name__ == '__main__':
	app.run()
