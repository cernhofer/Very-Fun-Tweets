from push_to_postgres import push_to_postgres
from scraping.news_scraper import run_baby_run
from scraping.tweet_scraper import run_for_your_life
from spikes import spikes
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os, json

load_dotenv(find_dotenv())
MONGODB_URI = os.environ.get("MONGODB_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

hashtags = db.tweets.find({})
for hashtag in hashtags:
    if len(hashtag['tweets']) < 1000: continue

    print("Here is Sush!")
    has_spike, date_list, spike_data = spikes(hashtag)

    if has_spike:
        print("SPIKE!")
        hashtag_name = spike_data['hashtag']
        print(hashtag_name)
        # get a list of strings of twitter texts
        tweet_text_list = tweet_text(hashtag)
        # pass to tweet scraping
        common_words = run_for_your_life(tweet_text_list)
        # pass to news scraping
        spike_data['stories'] = run_baby_run(hashtag_name, date_list, common_words)

        push_to_postgres(spike_data)

def tweet_text(hashtag):
    tweet_text_list = []
    tweets = hashtag['tweets']
    for tweet in tweets:
        tweet_text_list.append(tweet['tweet_text'])

    return tweet_text_list
