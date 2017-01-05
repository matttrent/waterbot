import requests
import io
import datetime as dt
import numpy as np
import pandas as pd


# http://cdec.water.ca.gov/cgi-progs/queryCSV
# ?station_id=hth
# &sensor_num=15
# &dur_code=D
# &start_date=2016-12-01
# &end_date=2016-12-27
# &data_wish=View+CSV+Data
DATA_URL = 'http://cdec.water.ca.gov/cgi-progs/queryCSV'


def get_reservoir_storage(station_id, sensor_num=15, dur_code='D', start_date=None, end_date=None):
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
	df = df[df.reservoir_storage >= 100]

	return df
