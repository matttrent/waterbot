import requests
import io
import datetime as dt
import numpy as np
import pandas as pd

from waterbot import config


def fetch_reservoir_storage(
	station_id, sensor_num=15, dur_code='D', start_date=None, end_date=None):
	"""

	"""

	if end_date is None:
		end_date = dt.date.today()

	if start_date is None:
		start_date = end_date - dt.timedelta(days=30)

	if start_date >= end_date:
		start_date = end_date - dt.timedelta(days=1)

	payload = dict(
		station_id=station_id, 
		sensor_num=sensor_num, 
		dur_code=dur_code, 
		start_date=start_date.isoformat(),
		end_date=end_date.isoformat(),
		data_wish='View CSV Data'
	)

	r = requests.get(config.RESERVOIR_DATA_URL, params=payload)
	csv_str = io.StringIO(r.text)

	df = pd.read_csv(
		csv_str, 
		header=1, 
		names=['date', 'time', 'reservoir_storage'],
		parse_dates=['date'])
	df.replace('m', np.nan, inplace=True)
	df.dropna(inplace=True)
	df.reservoir_storage = df.reservoir_storage.astype(float)
	df = df[df.reservoir_storage >= 100]

	return df


def fetch_all_reservoirs(
	reservoirs,
	start_date=config.HISTORICAL_START_DATE,
	end_date=config.HISTORICAL_END_DATE):

	results = {}
	for reservoir in reservoirs:
		station_id = reservoir['station_id']

		# fetch reservoir data, reattempting until success
		keep_trying = True
		while keep_trying:
			try:
				df = fetch_reservoir_storage(
					station_id=station_id,
					start_date=start_date,
					end_date=end_date
				)
				keep_trying = False
			except requests.exceptions.ConnectionError:
				pass
 
		results[station_id] = df

	return results
