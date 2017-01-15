import os
import datetime as dt


DATA_DIR 				= 'data'

HISTORICAL_START_DATE 	= dt.date(1990, 1, 1)
HISTORICAL_END_DATE		= dt.date.today()
SEASONAL_START_DATE 	= dt.date(1990, 1, 1)
SEASONAL_END_DATE		= dt.date(2010, 12, 31)


HISTORICAL_LEVELS_DIR 	= os.path.join(DATA_DIR, 'historical_levels')
SEASONAL_AVERAGE_DIR 	= os.path.join(DATA_DIR, 'seasonal_averages')

PRIMARY_RESERVOIR_LIST 	= 'reservoirs.json'
ALL_RESERVOIR_LIST 		= 'reservoirs_all.json'

RESERVOIR_LIST_URL 		= 'http://cdec.water.ca.gov/cgi-progs/reservoirs/RES'

# http://cdec.water.ca.gov/cgi-progs/queryCSV
# ?station_id=hth
# &sensor_num=15
# &dur_code=D
# &start_date=2016-12-01
# &end_date=2016-12-27
# &data_wish=View+CSV+Data
RESERVOIR_DATA_URL 		= 'http://cdec.water.ca.gov/cgi-progs/queryCSV'
