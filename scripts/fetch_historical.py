#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests

import datetime as dt
import pandas as pd

from waterbot import config, water_api


if __name__ == '__main__':

	if not os.path.exists(config.HISTORICAL_LEVELS_DIR):
	    os.makedirs(config.HISTORICAL_LEVELS_DIR)

	reservoirs = json.load(open(config.ALL_RESERVOIR_LIST))

	for reservoir in reservoirs:

		print reservoir['station_id'],

		keep_trying = True
		while keep_trying:
			try:
				df = water_api.get_reservoir_storage(
					station_id=reservoir['station_id'],
					start_date=HISTORICAL_START_DATE,
					end_date=HISTORICAL_END_DATE
				)
				keep_trying = False
			except requests.exceptions.ConnectionError:
				print '.',

		df.to_csv(
			os.path.join(
				config.HISTORICAL_LEVELS_DIR,
				'{station_id}.csv'.format(
					station_id=reservoir['station_id'])
			),
			index=False
		)

		print
