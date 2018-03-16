#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script will run every half of hour to fetch every tweet that was
twitted on source account and then save them in a Postgre database
"""

import strings
from flask import Flask
from database import Database
from models import Tweet
from twitter_api import TwitterAPI
from datetime import datetime

print("- INITIALIZING SCRIPT TO FETCH TWEETS ")
print("HORA CERTA ROGERINHO: %s" % (str(datetime.now())))
app = Flask(__name__)

print("- INSTANTIATING DATABASE ")
database = Database(app)

print("- INSTANTIATING TWITTER API")
source_twitter = TwitterAPI(strings.SOURCE, database)

print("- GETTING TWEET LIST")
tweet_list = source_twitter.get_timeline_tweets()

print("- SAVE TWEETS TO THE DATABASE")
if(tweet_list):
	print("- %d TWEETS FETCHED" % (len(tweet_list)))
	for tweet in tweet_list:
		tweet_id = str(tweet['id'])
		text = tweet['text']
		origin = tweet['origin']
		sentiment = 0
		tweet = Tweet(tweet_id, text, sentiment, origin)
		database.post_tweet(tweet)
		print(" - TWEET %s SAVED TO DATABASE WITH SUCCESS" % (tweet_id))





