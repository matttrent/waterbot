#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import datetime as dt
import pandas as pd

from waterbot import water_api


START_DATE 	= dt.date(1990, 1, 1)
END_DATE	= dt.date(2016, 12, 31)
DIRECTORY 	= 'historical_levels'


if __name__ == '__main__':

	if not os.path.exists(DIRECTORY):
	    os.makedirs(DIRECTORY)

	reservoirs = json.load(open('reservoirs_all.json'))

	for reservoir in reservoirs:
		df = water_api.get_reservoir_storage(
			station_id=reservoir['station_id'],
			start_date=START_DATE,
			end_date=END_DATE
		)

		df.to_csv(
			os.path.join(
				DIRECTORY,
				'{station_id}.csv'.format(
					station_id=reservoir['station_id'])
			),
			index=False
		)

		print reservoir['station_id']
