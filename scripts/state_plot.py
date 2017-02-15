#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import json
import tempfile
import requests

import datetime as dt
import numpy as np
import pandas as pd

from waterbot import config, water_api, seasonal, twitter, util

import matplotlib as mpl
if util.environment() == 'production':
    mpl.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns


sns.set_style('white')


def fetch_reservoir_data(reservoirs, first_day, today):

    dfs = water_api.fetch_all_reservoirs(
        reservoirs, first_day, today)

    for res_name in dfs.keys():
        dfs[res_name] = seasonal.forwardfill_missing_dates(dfs[res_name]) 

    dfc = seasonal.daily_state_totals(
        dfs, first_day, today, concat=True)

    return dfc


def load_seasonal_data():

    infile = os.path.join(
        config.SEASONAL_AVERAGE_DIR,
        config.STATE_STATISTICS)
    seasonal = pd.read_csv(infile, index_col='day_of_year')

    seasonal = (
        seasonal
        [seasonal.index <= 365]
        .copy()
        .rolling(5, center=True)
        .mean()
    )

    return seasonal


def create_plot_data(dfc, seasonal, first_day, last_day):

    dates = pd.Series( pd.date_range(first_day, last_day, freq='D') )

    plot_df = (
        dfc
        .set_index('date')
        .reindex(dates)
    )

    plot_df['day_of_year'] = pd.Series(plot_df.index, index=plot_df.index).apply(
        lambda d: d.timetuple().tm_yday
    )

    plot_df = (
        pd.merge(
            plot_df,
            seasonal,
            how='left',
            left_on='day_of_year',
            right_index=True
        )
        .interpolate()
    )

    return plot_df


def plot_figure(plot_df):

    fig, ax = plt.subplots(1, figsize=(8,8))

    min_level = .85 * min( plot_df.reservoir_storage.min(), plot_df.lo.min() )
    max_level = 1.1 * max( plot_df.reservoir_storage.max(), plot_df.whoa.max() )

    ax.fill_between(plot_df.index, min_level, plot_df.lo, facecolor='red', alpha=0.4, linewidth=0)
    ax.fill_between(plot_df.index, plot_df.lo, plot_df.mid, facecolor='yellow', alpha=0.4, linewidth=0)
    ax.fill_between(plot_df.index, plot_df.mid, plot_df.hi, facecolor='#55cc00', alpha=0.4, linewidth=0)
    ax.fill_between(plot_df.index, plot_df.hi, plot_df.whoa, facecolor='green', alpha=0.4, linewidth=0)
    ax.fill_between(plot_df.index, plot_df.whoa, max_level, facecolor='teal', alpha=0.4, linewidth=0)

    plt.plot(
        plot_df[ plot_df.index <= pd.Timestamp(today) ].index,
        plot_df[ plot_df.index <= pd.Timestamp(today) ].reservoir_storage,
        color='black', linewidth=3
    )

    # plt.plot(plot_df.loc[today].name, plot_df.loc[today].reservoir_storage, 'ko')

    plt.ylim( min_level, max_level )

    plt.yticks(
        plot_df.iloc[0][['lo', 'mid', 'hi', 'whoa']],
        ['{}th percentile'.format(y) for y in [20, 40, 60, 80]]
    )

    plt.subplots_adjust(left=.15, bottom=.15, right=.95, top=.95)

    return fig


if __name__ == '__main__':
    
    today = dt.date.today()
    first_day = today - dt.timedelta(days=60)
    last_day  = today + dt.timedelta(days=30)

    reservoirs = json.load(open(config.ALL_RESERVOIR_LIST))

    dfc = fetch_reservoir_data(reservoirs, first_day, today)
    seasonal = load_seasonal_data()

    plot_df = create_plot_data(dfc, seasonal, first_day, last_day)

    fig = plot_figure(plot_df)

    fnum, filename = tempfile.mkstemp(suffix='.png')
    print filename

    if util.environment() == 'production':
        twapi = twitter.get_api()
        fig.savefig(filename)
        twapi.update_with_media(
            filename,
            'Total California reservoir water compared to historical levels.'
        )
    else:
        fig.savefig('test.png')
