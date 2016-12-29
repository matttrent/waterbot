import json
import peewee

from playhouse import migrate
from waterbot import models, database


def up():

	migrator = migrate.PostgresqlMigrator(database.get_connector())

	migrate.migrate(
		migrator.add_column('reservoir', 'latitude', peewee.FloatField(null=True)),
		migrator.add_column('reservoir', 'longitude', peewee.FloatField(null=True)),
		migrator.add_column('tweet', 'tweet_id', peewee.BigIntegerField(null=True))
	)

	reservoirs = json.load(open('reservoirs.json'))

	for reservoir in models.Reservoir.select():
		res_entries = [r for r in reservoirs if r['station_id'] == reservoir.station_id]

		if len(res_entries) > 0:
			res = res_entries[0]
			print res['latitude'], res['longitude']
			reservoir.latitude = res['latitude']
			reservoir.longitude = res['longitude']
			print reservoir.save()


def down():
	
	migrator = migrate.PostgresqlMigrator(database.get_connector())

	migrate.migrate(
		migrator.drop_column('reservoir', 'latitude'),
		migrator.drop_column('reservoir', 'longitude'),
		migrator.drop_column('tweet', 'tweet_id')
	)
