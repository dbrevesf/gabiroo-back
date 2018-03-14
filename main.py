#!/usr/bin/env python
# -*- coding: utf-8 -*-

import strings
import tweepy

from database import Database
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Tweets
from tweepy import OAuthHandler
from twitter_api import TwitterAPI


app = Flask(__name__)
database = Database(app)
source_twitter = TwitterAPI(strings.SOURCE, database)
destination_twitter = TwitterAPI(strings.DESTINATION, database)
CORS(app)


@app.route('/tweets', methods=['GET'])
def get_tweets():
	"""
		Call the twitter api to get up to 200 tweets from 
		source timeline.
                  
      	Return:
			json: the tweet list in json format.
           
	"""
	# getting source tweet list
	tweet_list = source_twitter.get_timeline_tweets()
	print("%d tweets were fetched" % (len(tweet_list)))
	return jsonify(tweet_list)


@app.route('/sentiment', methods=['POST'])
def post_sentiment():
	"""
		Post a sentiment about a single tweet.
                  
      	Return:
			json: a response sample
           
	"""
	tweetSentiment = {}
	if request.json:
		tweet_id = str(request.json['id'])
		text = request.json['text']
		origin = request.json['origin']
		sentiment = request.json['sentiment']
		if(sentiment == True):
			destination_twitter.post_tweet(text)
		tweetSentiment = Tweets(tweet_id, text, sentiment, origin)
		print("DEU BAO")

	return jsonify({'result': 'true'})




if __name__ == '__main__':
    app.run(debug=True)
