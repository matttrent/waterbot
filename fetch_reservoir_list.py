#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import pandas as pd


DATA_URL = 'http://cdec.water.ca.gov/cgi-progs/reservoirs/RES'


if __name__ == '__main__':

	df = pd.read_html(
		DATA_URL,
		header=0,
		skiprows=[0, 2]
		)[0]
	df = df.dropna()

	reservoirs = []
	for idx, ser in df.iterrows():

		capacity = int(ser['Capacity(AF)'])
		d = {
			'station_id':		ser['StaID'].lower(),
			'name':				ser['Reservoir Name'].lower(),
			'capacity':			capacity,
		}
		reservoirs.append(d)

	with open('reservoirs_all.json', 'w') as outfile:
		json.dump(reservoirs, outfile, indent=4, separators=(',', ': '))
