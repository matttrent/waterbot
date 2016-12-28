import json

from waterbot import models, util


def up():

	reservoirs = json.load(open('reservoirs.json'))
	for res in reservoirs:
		models.Reservoir.create(
			station_id=res['station_id'],
			name=res['name'],
			capacity=util.acrefeet_to_liters(res['capacity']),
			threshold=res['threshold']
		)


def down():
	models.Reservoir.delete().execute()
