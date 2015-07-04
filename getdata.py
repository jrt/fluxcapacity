#!/usr/bin/env python3
import requests
import json
import psycopg2

URL = 'https://www.googleapis.com/mapsengine/v1/tables/09372590152434720789-08620406515972909896/features'
KEY = 'AIzaSyDB3manTIJORPPJL06pKafXmO_KxPPKysE'


def getFeatures():
	req_params = {'version': 'published', 'key': KEY}
	while True:
		response = requests.get(URL, params=req_params)
		if not response.ok:
			raise Exception('Request failed: {}'.format(response))
		data = response.json()
		for feature in data['features']:
			yield feature
		if 'nextPageToken' not in data:
			return
		req_params['pageToken'] = data['nextPageToken']


def main():
	db = psycopg2.connect(dbname='james')
	for feature in getFeatures():
		print(json.dumps(feature))


if __name__ == '__main__':
	main()
