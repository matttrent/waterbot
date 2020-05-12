import os
import datetime as dt


DATA_DIR 				= 'data'

HISTORICAL_START_DATE 	= dt.date(1990, 1, 1)
HISTORICAL_END_DATE		= dt.date.today()
SEASONAL_START_DATE 	= dt.date(1990, 1, 1)
SEASONAL_END_DATE		= dt.date(2009, 12, 31)


HISTORICAL_LEVELS_DIR 	= os.path.join(DATA_DIR, 'historical_levels')
SEASONAL_AVERAGE_DIR 	= os.path.join(DATA_DIR, 'seasonal_averages')

PRIMARY_RESERVOIR_LIST 	= 'reservoirs.json'
ALL_RESERVOIR_LIST 		= 'reservoirs_all.json'

STATE_STATISTICS        = 'california.json'

RESERVOIR_LIST_URL 		= 'http://cdec.water.ca.gov/cgi-progs/reservoirs/RES'

# http://cdec.water.ca.gov/dynamicapp/req/JSONDataServlet
# ?Stations=hth
# &SensorNums=15
# &dur_code=D
# &Start=2016-12-01
# &End=2016-12-27
RESERVOIR_DATA_URL 		= 'http://cdec.water.ca.gov/dynamicapp/req/JSONDataServlet'
