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

	results = water_api.fetch_all_reservoirs(reservoirs)

	for station_id, df in results.items():

		outfile = os.path.join(
			config.HISTORICAL_LEVELS_DIR,
			'{station_id}.csv'.format(
				station_id=station_id)
		)
		df.to_csv(outfile, index=False)
