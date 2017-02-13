#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import datetime as dt
import numpy as np
import pandas as pd

from waterbot import config


def constrain_date_range(df, start_date, end_date):
    return df[
          (df.date >= start_date)
        & (df.date <= end_date)
    ].copy()


def clean_data(df, station_id, 
    start_date=config.SEASONAL_START_DATE, 
    end_date=config.SEASONAL_END_DATE):

    all_dates = pd.Series( pd.date_range(start_date, end_date, freq='D') )
    
    # constrain to date range, get rid of unneeded columns
    df = (
        constrain_date_range(df, start_date, end_date)
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
    to_fill['station_id'] = station_id

    # interpolate values    
    to_fill = to_fill.interpolate().fillna(0)

    # complete index
    to_fill.index.name = 'date'
    to_fill = to_fill.reset_index()

    return to_fill


def forwardfill_missing_dates(df):

    min_date = df.date.min()
    max_date = df.date.max()

    all_dates = pd.Series( pd.date_range(min_date, max_date, freq='D') )
    all_dates.name = 'date'

    to_fill = (
        df
        .set_index('date')
        .reindex(all_dates)
    )

    filled = to_fill.fillna(method='ffill')
    filled = filled.reset_index()

    return filled


def individual_average(df, 
    start_date=config.SEASONAL_START_DATE, 
    end_date=config.SEASONAL_END_DATE):
    
    # constrain to date range
    df = constrain_date_range(df, start_date, end_date)

    # compute day of year for each date
    df['day_of_year'] = df.date.apply(
        lambda x: x.timetuple().tm_yday)

    # average across all dates for each day of year
    seasonal_avg = (
        df
        .groupby('day_of_year', as_index=False)
        .agg({
            'reservoir_storage': 'mean'
        })
    )
    return seasonal_avg


def daily_state_totals(reservoirs, 
    start_date=config.SEASONAL_START_DATE, 
    end_date=config.SEASONAL_END_DATE,
    concat=False):

    all_res = reservoirs
    if concat:
        all_res = pd.concat(all_res.values())

    # constrain to date range
    # sum across all reservoirs for a given date
    state_total = (
        constrain_date_range(all_res, start_date, end_date)
        .groupby('date')
        .agg({
            'reservoir_storage': 'sum',
        })
        .reset_index()
    )

    # compute day of year for each date
    state_total['day_of_year'] = state_total.date.apply(
        lambda d: d.timetuple().tm_yday
    )

    return state_total


def day_of_year_stats(state_total):

    # group by day of year and compute percentiles
    return (
        state_total
        .groupby('day_of_year')
        .reservoir_storage
        .agg({
            'lo':   lambda x: np.percentile(x, 20),
            'mid':  lambda x: np.percentile(x, 40),
            'hi':   lambda x: np.percentile(x, 60),
            'whoa': lambda x: np.percentile(x, 80),
        })
    )
