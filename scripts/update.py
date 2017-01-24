#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests

import datetime as dt
import pandas as pd

from waterbot import config, models, util, twitter, water_api


def update_reservoir_storage(reservoir):

	try:
		storage_df = water_api.fetch_reservoir_storage(
			station_id=reservoir.station_id)
	except requests.ConnectionError:
		return

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


def tweet_changes(reservoir):

	last_measure = reservoir.measures.order_by(-models.StorageMeasure.date).get()

	tweets = reservoir.tweets.order_by(-models.Tweet.posted_at)

	last_tweet = None
	difference = 0
	storage_threshold = reservoir.capacity * reservoir.threshold

	if tweets.count() > 0:
		last_tweet = tweets.get()
		difference = last_measure.storage - last_tweet.measure.storage

	if last_tweet is not None and abs(difference) < storage_threshold:
		return

	direction = u'⬆'
	if difference < 0:
		direction = u'⬇'

	percent_capacity = 100 * last_measure.storage / last_measure.reservoir.capacity
	percent_capacity_diff = 100 * difference / last_measure.reservoir.capacity

	days_since_last_update_message = ''
	if last_tweet is not None:
		days_since_last = (last_measure.date - last_tweet.posted_at.date()).days
		days_since_last = max(days_since_last, 1)
		days = 'day'
		if days_since_last > 1:
			days = 'days' 
		days_since_last_update_message = ' in past {since_last} {days}'.format(
			since_last=days_since_last,
			days=days
		)

	day_of_year = last_measure.date.timetuple().tm_yday
	seasonal_avg_fn = os.path.join(
		config.SEASONAL_AVERAGE_DIR,
		'{station_id}.csv'.format(station_id=reservoir.station_id)
	)
	seasonal_avg = pd.read_csv(seasonal_avg_fn, index_col=0)
	seasonal_avg = seasonal_avg.loc[day_of_year].reservoir_storage
	seasonal_multiple = last_measure.storage / util.acrefeet_to_liters(seasonal_avg)

	storage = last_measure.storage / 1e9
	scale = 'billion'

	tweet = u'{reservoir}: {direction} {percent_diff:+2.1f}%{days_since}, now {percent_full:2.1f}% full. {seasonal_multiple:3.2f}x seasonal average.'.format(
		reservoir=reservoir.name,
		direction=direction,
		percent_diff=percent_capacity_diff,	
		days_since=days_since_last_update_message,
		percent_full=percent_capacity,
		seasonal_multiple=seasonal_multiple,
		storage=storage,
		scale=scale,
	)

	tweet_id = None
	if util.environment() == 'production':
		twapi = twitter.get_api()
		status = twapi.update_status(
			tweet, lat=reservoir.latitude, long=reservoir.longitude, 
			place_id=reservoir.twitter_place_id)
		tweet_id = status.id
	elif util.environment() == 'development':
		print len(tweet), '\t', tweet 

	models.Tweet.create(
		reservoir=reservoir,
		measure=last_measure,
		posted_at=dt.datetime.utcnow(),
		text=tweet,
		tweet_id=tweet_id
	)


def tweet_all_changes():

	reservoirs = models.Reservoir.select()
	for reservoir in reservoirs:
		tweet_changes(reservoir)


if __name__ == '__main__':

	update_all_reservoirs()
	tweet_all_changes()
