#!/usr/bin/env python
import json
import requests
import sys
import time

URL = 'http://localhost:8000'

def main():
	demodata = open('demodata.json').readline()
	print demodata

	while True:
		response = requests.get(URL + '/pie')
		if not response.ok:
			print >> sys.stderr, "bad response: {}".format(response)
			time.sleep(2)
			continue
		data = response.json()
		#print >> sys.stderr, "ok response: {}".format(data)
		tcsno = data['tcsno']
		t = data['time']
		response = requests.get('{}/piedata/{}/{}'.format(URL, tcsno, t))
		if not response.ok:
			print >> sys.stderr, "bad response: {}".format(response)
			time.sleep(2)
			continue
		data = response.json()
		print json.dumps(data)
		time.sleep(10)


if __name__ == '__main__':
	main()
