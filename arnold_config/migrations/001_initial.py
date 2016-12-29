from waterbot import database, models


def up():
	db = database.get_connector()
	db.create_tables([
		models.Reservoir,
		models.StorageMeasure,
		models.Tweet
	])


def down():
	models.Reservoir.drop_table(cascade=True)
	models.StorageMeasure.drop_table(cascade=True)
	models.Tweet.drop_table(cascade=True)
