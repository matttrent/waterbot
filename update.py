
import io
import datetime as dt
import requests
import numpy as np
import pandas as pd

from waterbot import models, util, twitter


# http://cdec.water.ca.gov/cgi-progs/queryCSV
# ?station_id=hth
# &sensor_num=15
# &dur_code=D
# &start_date=2016-12-01
# &end_date=2016-12-27
# &data_wish=View+CSV+Data
DATA_URL = 'http://cdec.water.ca.gov/cgi-progs/queryCSV'


def get_reservoir(station_id, sensor_num=15, dur_code='D', start_date=None, end_date=None):
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

	r = requests.get(DATA_URL, params=payload)
	csv_str = io.StringIO(r.text)

	df = pd.read_csv(
		csv_str, 
		header=1, 
		names=['date', 'time', 'reservoir_storage'],
		parse_dates=['date'])
	df.replace('m', np.nan, inplace=True)
	df.dropna(inplace=True)
	df.reservoir_storage = df.reservoir_storage.astype(float)

	return df


def update_reservoir_storage(reservoir):

	storage_df = get_reservoir(station_id=reservoir.station_id)

	storage_measures = (
		models.StorageMeasure.select()
		.where(models.StorageMeasure.reservoir == reservoir)
		.where(models.StorageMeasure.date >= storage_df.date.min())
	)

	logged_dates = [sm.date for sm in storage_measures]

	storage_df = storage_df[ ~storage_df.date.isin(logged_dates) ]

	for name, row in storage_df.iterrows():
		models.StorageMeasure.create(
			reservoir=reservoir,
			date=row.date,
			storage=util.acrefeet_to_liters(row.reservoir_storage)
		)

	print '{} added {} rows'.format(reservoir.station_id, len(storage_df))


def update_all_reservoirs():

	reservoirs = models.Reservoir.select()
	for reservoir in reservoirs:
		update_reservoir_storage(reservoir)


def tweet_results():

	sm = models.StorageMeasure.get()

	tweet = '{reservoir} current level: {storage:0.2f} billion liters'.format(
		reservoir=sm.reservoir.name,
		storage=sm.storage / 1e9
	)

	print tweet

	twapi = twitter.get_api()
	twapi.update_status(tweet)


if __name__ == '__main__':
	update_all_reservoirs()
	tweet_results()
