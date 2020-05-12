#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import pandas as pd

from waterbot import config


if __name__ == '__main__':

	# read html table from site and coerce into dataframe
	df = pd.read_html(
		config.RESERVOIR_LIST_URL,
		header=0,
		skiprows=[0]
		)[0]
	df = df.dropna()

	# discard rows indicating the region, as defined by the reservoir name
	# being present in other columns
	df = df[
		(df["Reservoir Name"] != df["Capacity(AF)"]) &
		(df["StaID"].apply(len) == 3)
	]

	# loop across all reservoir rows, create info dict
	reservoirs = []
	for idx, ser in df.iterrows():

		capacity = int(ser['Capacity(AF)'])
		d = {
			'station_id':		ser['StaID'].lower(),
			'name':				ser['Reservoir Name'].lower(),
			'capacity':			capacity,
		}
		reservoirs.append(d)

	# save to json
	with open(config.ALL_RESERVOIR_LIST, 'w') as outfile:
		json.dump(reservoirs, outfile, indent=4, separators=(',', ': '))
