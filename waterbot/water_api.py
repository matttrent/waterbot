import requests
import io
import datetime as dt
import numpy as np
import pandas as pd

from waterbot import config


def fetch_reservoir_storage(
	station_ids, sensor_num=15, dur_code='D', start_date=None, end_date=None):
	"""

	"""

	if type(station_ids) is not list:
		station_ids = [station_ids]

	if end_date is None:
		end_date = dt.date.today()

	if start_date is None:
		start_date = end_date - dt.timedelta(days=30)

	if start_date >= end_date:
		start_date = end_date - dt.timedelta(days=1)

	payload = dict(
		Stations=','.join(station_ids), 
		SensorNums=sensor_num, 
		dur_code=dur_code, 
		Start=start_date.isoformat(),
		End=end_date.isoformat(),
	)

	r = requests.get(config.RESERVOIR_DATA_URL, params=payload)
	resp_str = io.StringIO(r.text)

	df = pd.read_json(
		resp_str, 
		orient="records",
		# header=0, 
		# names=['date', 'time', 'reservoir_storage'],
		convert_dates=["date", "obsDate"])
	df = df[df["value"] >= 0]

	df = df.rename(
		columns={
			"stationId": "station_id",
			"durCode": "duration_code",
			"SENSOR_NUM": "sensor_num",
			"sensorType": "sensor_type",
			"obsDate": "observe_date",
			"dataFlag": "data_flag",
		}
	)
	df["reservoir_storage"] = df["value"]

	return df


def fetch_all_reservoirs(
	reservoirs,
	start_date=config.HISTORICAL_START_DATE,
	end_date=config.HISTORICAL_END_DATE):

	station_ids = [res["station_id"] for res in reservoirs]

	keep_trying = True
	while keep_trying:
		try:
			df = fetch_reservoir_storage(
				station_ids=station_ids,
				start_date=start_date,
				end_date=end_date
			)
			keep_trying = False
		except requests.exceptions.ConnectionError:
			pass

	results = {}
	for station_id in station_ids:
		results[station_id] = df[df.station_id.str.lower() == station_id.lower()]

	return results
