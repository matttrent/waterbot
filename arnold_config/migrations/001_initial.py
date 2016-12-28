from waterbot import database, models


def up():
	db = database.get_connector()
	db.create_tables([
		models.Reservoir,
		models.StorageMeasure,
		models.Tweet
	])


def down():
	models.Reservoir.delete()
	models.StorageMeasure.delete()
	models.Tweet.delete()
