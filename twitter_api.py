#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import strings
import tweepy

from database import Database
from database_sample import TWEET_SAMPLES
from secured_credentials import *


class TwitterAPI():

	twitter_api = None
	database = None

	def __init__(self, origin, database):

		# authenticating tweepy accounts
		consumer_key = GABIROO_TWITTER_CONSUMER_KEY
		consumer_secret = GABIROO_TWITTER_CONSUMER_SECRET
		access_token_key = GABIROO_TWITTER_ACCESS_TOKEN_KEY
		access_token_secret = GABIROO_TWITTER_ACCESS_TOKEN_SECRET
		if origin == strings.SOURCE:
			consumer_key = SOURCE_TWITTER_CONSUMER_KEY
			consumer_secret = SOURCE_TWITTER_CONSUMER_SECRET
			access_token_key = SOURCE_TWITTER_ACCESS_TOKEN_KEY
			access_token_secret = SOURCE_TWITTER_ACCESS_TOKEN_SECRET

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token_key, access_token_secret)
		self.twitter_api = tweepy.API(auth)
		self.database = database


	def get_timeline_tweets(self):
		"""
			Get up to 200 tweets from the source timeline
			and update the current maximum id in order to
			avoid fetching already fetched tweets. 
                 
      		Return:
                list: tweets from the source timeline
        """
		# getting the current minimum ID
		minimum_id = self.database.get_current_minimum_id()
		minimum_id_value = int(minimum_id.value)

		# building the tweet list with object
		tweet_list = []
		current_maximum_id = 0
		
		try:
			for status in tweepy.Cursor(self.twitter_api.home_timeline, 
										since_id=minimum_id_value).items(200):
				# getting the current maximum id
				if(status.id > minimum_id_value):
					minimum_id_value = status.id
					current_maximum_id = minimum_id_value
					
				tweet = {"text":status.text,
						 "id": status.id,
						 "origin": status.user.name}
				tweet_list.append(tweet)
				
		except tweepy.error.TweepError:
			print(datetime.datetime.now())

	

		# updating minimum ID
		self.database.update_current_minimum_id(minimum_id, 
												current_maximum_id)

		return tweet_list


	def post_tweet(self, tweet):
		"""
			Post a single tweet in the Gabiroo timeline.

			Args:
				tweet (string): the tweet to be posted
        """
		self.twitter_api.update_status(tweet)








