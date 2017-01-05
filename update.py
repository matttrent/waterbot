#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime as dt

from waterbot import models, util, twitter, water_api


def update_reservoir_storage(reservoir):

	try:
		storage_df = water_api.get_reservoir_storage(
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

	direction = u'increased ⬆️'
	if difference < 0:
		direction = u'decreased ⬇️'

	storage = last_measure.storage / 1e9
	scale = 'billion'
	percent = 100 * last_measure.storage / last_measure.reservoir.capacity

	tweet = u'{reservoir} {direction} to {storage:0.0f} {scale} liters, {percent:2.1f}% full.'.format(
		reservoir=reservoir.name,
		direction=direction,
		storage=storage,
		scale=scale,
		percent=percent
	)

	tweet_id = None
	if util.environment() == 'production':
		twapi = twitter.get_api()
		status = twapi.update_status(
			tweet, lat=reservoir.latitude, long=reservoir.longitude, 
			place_id=reservoir.twitter_place_id)
		tweet_id = status.id
	elif util.environment() == 'development':
		print tweet

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
