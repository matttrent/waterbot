import peewee

from waterbot import database, twitter


class BaseModel(peewee.Model):

	class Meta:
		database = database.get_connector()


class Reservoir(BaseModel):

	station_id = peewee.CharField()
	name = peewee.CharField()
	capacity = peewee.FloatField()
	threshold = peewee.FloatField(default=.02)
	latitude = peewee.FloatField(null=True)
	longitude = peewee.FloatField(null=True)
	nearest_city = peewee.CharField()
	twitter_place_id = peewee.CharField()


class StorageMeasure(BaseModel):

	reservoir = peewee.ForeignKeyField(Reservoir, related_name='measures')
	date = peewee.DateField()
	storage = peewee.FloatField()


class Tweet(BaseModel):

	text = peewee.TextField()
	posted_at = peewee.DateTimeField()
	reservoir = peewee.ForeignKeyField(Reservoir, related_name='tweets')
	measure = peewee.ForeignKeyField(StorageMeasure, related_name='tweets')
	tweet_id = peewee.BigIntegerField(null=True)

	def delete_instance(**kwargs):
		
		if self.tweet_id is not None:
			twapi = twitter.get_api()
			try:
				twapi.destroy_status(self.tweet_id)
			except:
				pass

		super(Tweet, self).delete_instance(**kwargs)
