#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import datetime as dt
import pandas as pd

from waterbot import config


def individual_reservoir(df, 
	start_date=config.SEASONAL_START_DATE, 
	end_date=config.SEASONAL_END_DATE):

	df = df[
		  (df.date >= start_date)
		& (df.date <= end_date)
	].copy()

	df['day_of_year'] = df.date.apply(
		lambda x: x.timetuple().tm_yday)

	seasonal_avg = (
		df
		.groupby('day_of_year', as_index=False)
		.agg({
			'reservoir_storage': 'mean'
		})
	)
	return seasonal_avg


def compute_individuals(reservoirs):

	for station_id, df in reservoirs.iteritems():

		seasonal_avg = individual_reservoir(df)
		
		outfile = os.path.join(
			config.SEASONAL_AVERAGE_DIR,
			'{station_id}.csv'.format(station_id=station_id)
		)
		seasonal_avg.to_csv(outfile, index=False)

		print station_id, 


def load_reservoirs(reservoir_filename=config.ALL_RESERVOIR_LIST):

	reservoir_map = {}
	reservoirs = json.load(open(config.ALL_RESERVOIR_LIST))

	for reservoir in reservoirs:
		station_id = reservoir['station_id']
		infile = os.path.join(
			config.HISTORICAL_LEVELS_DIR,
			'{station_id}.csv'.format(station_id=station_id)
		)
		reservoir_map[station_id] = pd.read_csv(infile, parse_dates=['date'])

	return reservoir_map


if __name__ == '__main__':

	if not os.path.exists(config.SEASONAL_AVERAGE_DIR):
	    os.makedirs(config.SEASONAL_AVERAGE_DIR)

	reservoirs = load_reservoirs()

	compute_individuals(reservoirs)
	# compute_aggregate(reservoirs)

