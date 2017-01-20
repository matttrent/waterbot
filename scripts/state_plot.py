#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import json

import datetime as dt
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

from waterbot import config


sns.set_style('white')


if __name__ == '__main__':
    
    today = pd.Timestamp(dt.date.today())
    first_day = today - dt.timedelta(days=60)
    last_day  = today + dt.timedelta(days=30)

    dates = pd.Series( pd.date_range(first_day, last_day, freq='D') )

    # plot_df = (
    #     df[ (df.date >= first_day) ]
    #     .set_index('date')
    #     .reindex(dates)
    # )

    # plot_df['day_of_year'] = pd.Series(plot_df.index, index=plot_df.index).apply(
    #     lambda d: d.timetuple().tm_yday
    # )

    plot_df = pd.DataFrame({
        'date': dates
    })
    plot_df['day_of_year'] = plot_df.date.apply(
        lambda d: d.timetuple().tm_yday)
    plot_df.set_index('date', inplace=True)

    # plot_df['day_of_year'] = plot_df.index.apply(
    #     lambda d: d.timetuple().tm_yday)

    infile = os.path.join(
        config.SEASONAL_AVERAGE_DIR,
        config.STATE_STATISTICS)
    shades = pd.read_csv(infile, index_col='day_of_year')

    shades2 = (
        shades
        [shades.index <= 365]
        .copy()
        .rolling(5, center=True)
        .mean()
    )

    plot_df = (
        pd.merge(
            plot_df,
            shades2,
            how='left',
            left_on='day_of_year',
            right_index=True
        )
        .interpolate()
    )

    fig, ax = plt.subplots(1, figsize=(8,8))

    # min_level = .85 * min( plot_df.reservoir_storage.min(), plot_df.lo.min() )
    # max_level = 1.1 * max( plot_df.reservoir_storage.max(), plot_df.hi.max() )
    min_level = .85 * plot_df.lo.min()
    max_level = 1.1 * plot_df.hi.max()

    ax.fill_between(plot_df.index, min_level, plot_df.lo, facecolor='red', alpha=0.4, linewidth=0)
    ax.fill_between(plot_df.index, plot_df.lo, plot_df.mid, facecolor='yellow', alpha=0.4, linewidth=0)
    ax.fill_between(plot_df.index, plot_df.mid, plot_df.hi, facecolor='#55cc00', alpha=0.4, linewidth=0)
    ax.fill_between(plot_df.index, plot_df.hi, max_level, facecolor='green', alpha=0.4, linewidth=0)

    # plt.plot(
    #     plot_df[ plot_df.index <= today ].index,
    #     plot_df[ plot_df.index <= today ].reservoir_storage,
    #     color='black', linewidth=3
    # )

    # plt.plot(plot_df.loc[today].name, plot_df.loc[today].reservoir_storage, 'ko')

    plt.ylim( min_level, max_level )

    plt.yticks(
        plot_df.iloc[0][['lo', 'mid', 'hi']],
        ['{}th percentile'.format(y) for y in [20, 40, 60]]
    )

    fig.savefig('test.png')
