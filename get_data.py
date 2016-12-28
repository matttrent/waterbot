
import io
import datetime as dt
import requests
import numpy as np
import pandas as pd


ACRE_FEET_TO_LITERS = 1233481.85532

RESERVOIRS = {
	'cle':	{
		'name':		'Trinity Lake',
		'capacity':	2447650,
	},
	'sha':	{
		'name':		'Lake Shasta',
		'capacity':	4552000,
	},
	'oro':	{
		'name':		'Lake Oroville',
		'capacity':	3537577,
	},
	'fol':	{
		'name':		'Folsom Lake',
		'capacity':	977000,
	},
	'nml':	{
		'name':		'New Melones Lake',
		'capacity':	2400000,
	},
	'dnp':	{
		'name':		'Don Pedro Reservoir',
		'capacity':	2030000,
	},
	'exc':	{
		'name':		'Lake McClure',
		'capacity':	1024600,
	},
	'snl':	{
		'name':		'San Luis Reservoir',
		'capacity':	2041000,
	},
	'mil':	{
		'name':		'Millerton Lake',
		'capacity':	520500,
	},
	'pnf':	{
		'name':		'Pine Flat Reservoir',
		'capacity':	1000000,
	},
	'prr':	{
		'name':		'Lake Perris',
		'capacity':	131452,
	},
	'cas':	{
		'name':		'Castaic Lake',
		'capacity':	325000,
	},
	'hth':	{
		'name':		'Hetch Hetchy',
		'capacity':	360000,
	},
}

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


for station_id in RESERVOIRS.keys():
	current_storage = get_reservoir(station_id=station_id).iloc[-1]['reservoir_storage']
	print( station_id, current_storage / RESERVOIRS[station_id]['capacity'] )
