from push_to_postgres import push_to_postgres
from scraping.news_scraper import run_baby_run
from scraping.tweet_scraper import run_for_your_life
from multiple_spikes_2_thresholds import spikes
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os, json

load_dotenv(find_dotenv())
MONGODB_URI = os.environ.get("MONGODB_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

total_count = 15861
hashtag_count = 0

while True:
    try:
        hashtags = db.tweets.find({}).skip(total_count)

        for hashtag in hashtags:
            hashtag_count += 1
            print("\n\n\nThis is hashtag number", hashtag_count)

            if len(hashtag['tweets']) < 1000: continue

            has_spike, date_list, spike_data, tweet_text_list = spikes(hashtag)

            if has_spike:
                print("SPIKE!!")
                hashtag_name = spike_data['hashtag']
                print(hashtag_name)

                common_words = run_for_your_life(tweet_text_list, hashtag_name)
                if common_words is not None:
                    print('Calling run_baby_run')
                    news_story = run_baby_run(hashtag_name, date_list, common_words)

                    if news_story is not None:
                        spike_data['stories'] = news_story

                        print('Pushing to postgres')
                        push_to_postgres(spike_data)
                else:
                    print("hashtag isn't news worthy :/")
    except pymongo.errors.CursorNotFound:
        total_count = total_count + hashtag_count
        hashtag_count = 0
