
# Gabiroo Project

This project is being developed as a filter of good news, based on my own definition of good. My aim with this project is to implement a Natural Language Processing (NLP) algorithm which will select, based on past news and my classification, some good news and post them on a Twitter account (@projeto_gabiroo).

## gabiroo_back

It's the backend part of the main project. I'm developing it with Python and using the web framework Flask. To obtain the tweets, the library Tweepy is also being used. Besides that, PostgreSQL was the choice for the relational database. 

## service to fetch tweets

It was necessary to write a service to run every 30 minutes in order to improve the extration of data. It was possible using Crontab.

Here's the Crontab configuration to run fetch_tweets.py every 30 minutes and save a log in the script_output.log file:

```
MAILTO=""
*/30 * * * *  ~/projects/gabiroo/gabiroo-env/bin/python ~/projects/gabiroo/gabiroo-back/fetch_tweets.py >> ~/projects/gabiroo/gabiroo-back/script_output.log 2>&1
```
