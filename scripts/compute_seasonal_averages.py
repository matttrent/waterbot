#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import datetime as dt
import pandas as pd

from waterbot import config


START_DATE 	= dt.date(1990, 1, 1)
END_DATE	= dt.date(2010, 12, 31)


if __name__ == '__main__':

	if not os.path.exists(config.SEASONA_AVERAGE_DIR):
	    os.makedirs(config.SEASONA_AVERAGE_DIR)

	reservoirs = json.load(open(config.ALL_RESERVOIR_LIST))

	for reservoir in reservoirs:

		station_id = reservoir['station_id']
		infile = os.path.join(
			config.HISTORICAL_LEVELS_DIR,
			'{station_id}.csv'.format(station_id=station_id)
		)
		outfile = os.path.join(
			config.SEASONA_AVERAGE_DIR,
			'{station_id}.csv'.format(station_id=station_id)
		)

		df = pd.read_csv(infile, parse_dates=['date'])

		df = df[
			  (df.date >= START_DATE)
			& (df.date <= END_DATE)
		]

		df['day_of_year'] = df.date.apply(
			lambda x: x.timetuple().tm_yday)

		seasonal_avg = (
			df
			.groupby('day_of_year', as_index=False)
			.agg({
				'reservoir_storage': 'mean'
			})
		)

		seasonal_avg.to_csv(outfile, index=False)

		print reservoir['station_id'], 
