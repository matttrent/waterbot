import os
import urlparse
import peewee


def get_connector(_cache=[]):
	if len(_cache) > 0:
		return _cache[0]

	database_url = os.environ.get('DATABASE_URL')
	urlp = urlparse.urlparse(database_url)

	database = peewee.PostgresqlDatabase(
		urlp.path[1:],
		host=urlp.hostname,
		user=urlp.username,
		password=urlp.password,
		port=urlp.port
	)
	database.connect()

	_cache.append(database)
	return database
