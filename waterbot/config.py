import os


DATA_DIR 				= 'data'

HISTORICAL_LEVELS_DIR 	= os.path.join(DATA_DIR, 'historical_levels')
SEASONA_AVERAGE_DIR 	= os.path.join(DATA_DIR, 'seasonal_averages')

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
