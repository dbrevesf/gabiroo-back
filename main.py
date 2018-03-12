from flask import Flask, jsonify
from flask_cors import CORS
import tweepy
from tweepy import OAuthHandler
from credencials import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET
from database import TWEET_SAMPLES

app = Flask(__name__)
CORS(app)

@app.route('/tweets', methods=['GET'])
def get_tweets():

	auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
	auth.set_access_token(TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)
	tweetlist = []
	#get the current maximum id
	current_maximum_id = 1
	# store the current maximum id
	try:
		for status in tweepy.Cursor(api.home_timeline).items(200):
			current_maximum_id = status.id if status.id > current_maximum_id else current_maximum_id
			tweet = {"text":status.text,
					 "id": status.id,
					 "origin": status.user.name}
			tweetlist.append(tweet)
	except tweepy.error.TweepError as e:
		print("TWEET SAMPLES")
		tweetlist = TWEET_SAMPLES

	return jsonify(tweetlist)

if __name__ == '__main__':
    app.run(debug=True)