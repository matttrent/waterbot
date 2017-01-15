#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import datetime as dt
import numpy as np
import pandas as pd

from waterbot import config


def individual_average(df, 
    start_date=config.SEASONAL_START_DATE, 
    end_date=config.SEASONAL_END_DATE):

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

        seasonal_avg = individual_average(df)

        outfile = os.path.join(
            config.SEASONAL_AVERAGE_DIR,
            '{station_id}.csv'.format(station_id=station_id)
        )
        seasonal_avg.to_csv(outfile, index=False)

        print station_id, 


def clean_data(df, station_id, 
    start_date=config.SEASONAL_START_DATE, 
    end_date=config.SEASONAL_END_DATE):

    all_dates = pd.Series( pd.date_range(start_date, end_date, freq='D') )
    
    # constrain to date range, get rid of unneeded columns
    df = (
        df[
              (df.date >= start_date)
            & (df.date <= end_date)
        ]
        .drop('time', axis=1)
        .copy()
    )
    
    # reindex the data to include every day in date range
    to_fill = (
        df
        .set_index('date')
        .reindex(all_dates)
    )
    
    # create rolling mean for comparison
    rmed = to_fill.rolling(20, min_periods=1, center=True).median()

    # declare every 
    to_fill.loc[
          (to_fill.reservoir_storage < .9  * rmed.reservoir_storage)
        | (to_fill.reservoir_storage > 1.1 * rmed.reservoir_storage),
        'reservoir_storage'
    ] = np.nan
    
    # set station_id
    df['station_id'] = station_id
    
    to_fill = to_fill.interpolate()
    to_fill.index.name = 'date'

    return to_fill.reset_index()


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

    for station_id in reservoirs:
        reservoirs[station_id] = clean_data(reservoirs[station_id], station_id)

    compute_individuals(reservoirs)
    # compute_aggregate(reservoirs)

