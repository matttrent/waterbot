import peewee

from waterbot import database


class BaseModel(peewee.Model):

	class Meta:
		database = database.get_connector()


class Reservoir(BaseModel):

	station_id = peewee.CharField()
	name = peewee.CharField()
	capacity = peewee.FloatField()
	threshold = peewee.FloatField(default=.02)


class StorageMeasure(BaseModel):

	reservoir = peewee.ForeignKeyField(Reservoir, related_name='measures')
	date = peewee.DateField()
	storage = peewee.FloatField()


class Tweet(BaseModel):

	text = peewee.TextField()
	posted_at = peewee.DateTimeField()
	reservoir = peewee.ForeignKeyField(Reservoir, related_name='tweets')
	measure = peewee.ForeignKeyField(StorageMeasure, related_name='tweets')

