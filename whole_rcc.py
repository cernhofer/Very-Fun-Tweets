from push_to_postgres import push_to_postgres
from scraping.news_scraper import run_baby_run
from scraping.tweet_scraper import run_for_your_life
from multiple_spikes_2_thresholds import spikes
import pymongo
from dotenv import load_dotenv, find_dotenv
import os, json

# variables that contain user credentials to access MongoDB
load_dotenv(find_dotenv())
MONGODB_URI = os.environ.get("MONGODB_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

client = pymongo.MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

# setting current total count and also hashtag count that resets for each
# iteration through the for loop below, in order to keep track of which data
# from the mongoDB has been processed
total_count = 0
hashtag_count = 0

# total number of hashtags in the MongoDB
num_hashtags = db.tweets.count()

# this while loop and try except is there for when the pymongo cursor times out
while total_count < num_hashtags:
    try:
        # skip to where we are in the database
        hashtags = db.tweets.find({}).skip(total_count)

        # iterate through each hashtag object and detect spikes and news stories
        # for any hashtags with greater than 1000 tweets
        for hashtag in hashtags:
            hashtag_count += 1

            if len(hashtag['tweets']) < 1000: continue

            has_spike, date_list, spike_data, tweet_text_list = spikes(hashtag)

            if has_spike:
                hashtag_name = spike_data['hashtag']
                print(hashtag_name)

                common_words = run_for_your_life(tweet_text_list, hashtag_name)
                if common_words is not None:
                    news_story = run_baby_run(hashtag_name, date_list, common_words)

                    if news_story is not None:
                        spike_data['stories'] = news_story

                        # push hashtag data to postgres if spike and news stories
                        # are both present
                        push_to_postgres(spike_data)

    # if cursor times out, update total_count, hashtag_count and restart
    except pymongo.errors.CursorNotFound:
        total_count = total_count + hashtag_count
        hashtag_count = 0
