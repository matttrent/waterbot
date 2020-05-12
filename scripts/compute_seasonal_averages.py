#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import datetime as dt
import numpy as np
import pandas as pd

from waterbot import config, seasonal


def load_reservoirs(reservoir_filename=config.ALL_RESERVOIR_LIST):

    reservoir_map = {}
    reservoirs = json.load(open(config.ALL_RESERVOIR_LIST))

    for reservoir in reservoirs:
        station_id = reservoir['station_id']
        infile = os.path.join(
            config.HISTORICAL_LEVELS_DIR,
            '{station_id}.json'.format(station_id=station_id)
        )
        reservoir_map[station_id] = pd.read_json(infile, orient="records")

    return reservoir_map


def compute_individuals(reservoirs):

    for station_id, df in reservoirs.items():

        seasonal_avg = seasonal.individual_average(df)

        outfile = os.path.join(
            config.SEASONAL_AVERAGE_DIR,
            '{station_id}.json'.format(station_id=station_id)
        )
        seasonal_avg.to_json(outfile, orient="records")

        print(station_id, end=" ")


def compute_aggregate(reservoirs, 
    start_date=config.SEASONAL_START_DATE, 
    end_date=config.SEASONAL_END_DATE):

    state_total = seasonal.daily_state_totals(
        reservoirs, start_date, end_date, concat=True)
    outfile = os.path.join(
        config.HISTORICAL_LEVELS_DIR,
        config.STATE_STATISTICS)
    state_total.to_json(outfile, orient="records")

    seasonal_stats = seasonal.day_of_year_stats(state_total)
    outfile = os.path.join(
        config.SEASONAL_AVERAGE_DIR,
        config.STATE_STATISTICS)
    seasonal_stats.to_json(outfile, orient="records")


if __name__ == '__main__':

    if not os.path.exists(config.SEASONAL_AVERAGE_DIR):
        os.makedirs(config.SEASONAL_AVERAGE_DIR)

    # load and clean data
    reservoirs = load_reservoirs()
    cleaned_reservoirs = {
        station_id: seasonal.clean_data(reservoir, station_id)
        for station_id, reservoir in reservoirs.items()
    }

    # compute reservoir stats
    compute_individuals(cleaned_reservoirs)
    compute_aggregate(cleaned_reservoirs)
