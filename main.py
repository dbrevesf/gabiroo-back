#!/usr/bin/env python
# -*- coding: utf-8 -*-

import strings
import tweepy

from database import Database
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Tweet
from tweepy import OAuthHandler
from twitter_api import TwitterAPI

BAD = 1
GOOD = 2
IGNORE = 3

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
	
	tweet_list = database.get_tweets()
	print("%d tweets were fetched" % (len(tweet_list)))
	response = []
	for tweet in tweet_list:
		response.append({'text': tweet.tweet,
						 'id': tweet.tweet_id,
						 'origin': tweet.origin})
	
	return jsonify(response)

@app.route('/goodnews', methods=['GET', 'POST'])
def good_news():
	"""
	GET
		Get all the tweets classified as good

	    Return:
	          list: list of tweets
	
	POST
		Publish a good news on destination Twitter account
		Return:
			json: a response sample
	"""
	response = None

	if request.method == 'POST':
		if(request.json):
			if 'text' and 'id' in request.json:
				good_news = request.json['text']
				tweet_id = request.json['id']
				database.update_tweet_sentiment(tweet_id, 4)
				destination_twitter.post_tweet(good_news)
		response = {'result': 'true'}

	elif request.method == 'GET':
		good_news = database.get_good_tweets()
		response = []
		for tweet in good_news:
			response.append({'text': tweet.tweet,
							 'id': tweet.tweet_id,
							 'origin': tweet.origin})

	return jsonify(response)


@app.route('/sentiment', methods=['POST'])
def post_sentiment():
	"""
		Post a sentiment about a single tweet.
                  
      	Return:
			json: a response sample
           
	"""
	if request.json:
		tweet_id = str(request.json['id'])
		sentiment = request.json['sentiment']
		database.update_tweet_sentiment(tweet_id, sentiment)
		
	return jsonify({'result': 'true'})





if __name__ == '__main__':
    app.run(debug=True)
