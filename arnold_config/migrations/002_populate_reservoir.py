import json

from waterbot import models, util


def up():

	reservoirs = json.load(open('reservoirs.json'))
	print reservoirs
	for res in reservoirs:
		print res
		models.Reservoir.create(
			station_id=res['station_id'],
			name=res['name'],
			capacity=util.acrefeet_to_liters(res['capacity'])
		)


def down():
	models.Reservoir.delete().execute()
