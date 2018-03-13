#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_cors import CORS
import tweepy
from tweepy import OAuthHandler
from secured_credentials import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET
from database import TWEET_SAMPLES
from models import Tweets, MinimumId
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/gabiroo_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
CORS(app)

@app.route('/tweets', methods=['GET'])
def get_tweets():

	auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
	auth.set_access_token(TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

	tweetlist = []
	#get the current maximum id
	current_maximum_id = db.session.query(func.max(MinimumId.minimum_id)).scalar()
	if(current_maximum_id):
		current_maximum_id = int(current_maximum_id)
	else:
		current_maximum_id = 1
	print("CURRENT MAXIMUM %s" % (current_maximum_id))
	try:
		for status in tweepy.Cursor(api.home_timeline, since_id=current_maximum_id).items(200):
			current_maximum_id = status.id if status.id > current_maximum_id else current_maximum_id
			tweet = {"text":status.text,
					 "id": status.id,
					 "origin": status.user.name}
			tweetlist.append(tweet)
		# store the current maximum id
		minimumId = MinimumId(str(current_maximum_id))
		db.session.add(minimumId)
		try:
			db.session.commit()
		except:
			print("MinimumId updated")

	except tweepy.error.TweepError as e:
		tweetlist = []

	print("%d tweets were fetched" % (len(tweetlist)))
	return jsonify(tweetlist)


@app.route('/sentiment', methods=['POST'])
def post_sentiment():

	tweetSentiment = {}
	if not request.json:
		print("DEU RUIM")
	else:
		tweet_id = str(request.json['id'])
		text = request.json['text']
		origin = request.json['origin']
		sentiment = request.json['sentiment']
		tweetSentiment = Tweets(tweet_id, text, sentiment, origin)
		db.session.add(tweetSentiment)
		db.session.commit()
		print("DEU BAO")

	return jsonify({'result': 'true'})


if __name__ == '__main__':
    app.run(debug=True)
