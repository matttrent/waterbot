#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import datetime as dt
import pandas as pd

from waterbot import config, water_api


START_DATE 	= dt.date(1990, 1, 1)
END_DATE	= dt.date.today()


if __name__ == '__main__':

	if not os.path.exists(config.HISTORICAL_LEVELS_DIR):
	    os.makedirs(config.HISTORICAL_LEVELS_DIR)

	reservoirs = json.load(open(config.ALL_RESERVOIR_LIST))

	for reservoir in reservoirs:
		df = water_api.get_reservoir_storage(
			station_id=reservoir['station_id'],
			start_date=START_DATE,
			end_date=END_DATE
		)

		df.to_csv(
			os.path.join(
				config.HISTORICAL_LEVELS_DIR,
				'{station_id}.csv'.format(
					station_id=reservoir['station_id'])
			),
			index=False
		)

		print reservoir['station_id']
