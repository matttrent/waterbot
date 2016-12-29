import json
import peewee

from playhouse import migrate
from waterbot import models, database


def up():

	migrator = migrate.PostgresqlMigrator(database.get_connector())

	migrate.migrate(
		migrator.add_column(
			'reservoir', 'nearest_city', peewee.CharField(null=True)),
		migrator.add_column(
			'reservoir', 'twitter_place_id', peewee.CharField(null=True))
	)

	res_list = json.load(open('reservoirs.json'))

	for reservoir in models.Reservoir.select():
		res_entries = [r for r in res_list if r['station_id'] == reservoir.station_id]

		if len(res_entries) > 0:
			res = res_entries[0]
			reservoir.nearest_city = res['nearest_city']
			reservoir.twitter_place_id = res['twitter_place_id']
			reservoir.save()


def down():
	
	migrator = migrate.PostgresqlMigrator(database.get_connector())

	migrate.migrate(
		migrator.drop_column('reservoir', 'nearest_city'),
		migrator.drop_column('reservoir', 'twitter_place_id')
	)
