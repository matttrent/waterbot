import json

import datetime as dt
import pandas as pd

from waterbot import water_api


START_DATE 	= dt.date(1995, 1, 1)
END_DATE	= dt.date(2016, 12, 31)


if __name__ == '__main__':

	reservoirs = json.load(open('reservoirs.json'))

	for reservoir in reservoirs:
		df = water_api.get_reservoir_storage(
			station_id=reservoir['station_id'],
			start_date=START_DATE,
			end_date=END_DATE
		)

		df.to_csv(
			'historical_levels/{station_id}.csv'.format(
				station_id=reservoir['station_id']
			),
		)
