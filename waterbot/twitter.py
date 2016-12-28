import os
import tweepy

def get_api(_cache=[]):

	if len(_cache) > 0:
		return _cache[0]

	consumer_key = os.environ.get('TWITTER_API_KEY')
	consumer_secret = os.environ.get('TWITTER_API_SECRET')
	access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
	access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	_cache.append(api)
	return api
