#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/gabiroo_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Create our database model
class Tweets(db.Model):

    __tablename__ = "tweets"
    tweet_id = db.Column(db.String, primary_key=True)
    tweet = db.Column(db.String(280))
    sentiment = db.Column(db.Boolean)
    origin = db.Column(db.String)

    def __init__(self, tweet_id, tweet, sentiment, origin):

    	self.tweet_id = tweet_id
    	self.tweet = tweet
    	self.sentiment = sentiment
    	self.origin = origin
    	
    def __repr__(self):
        return '<Tweet %s>' % self.tweet

class MinimumId(db.Model):

    __tablename__ = "minimum_id"
    value = db.Column(db.String, unique=True, primary_key=True)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<MinimumId %s>' % self.value


if __name__ == '__main__':
    app.debug = True
    app.run()