import os, json
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

load_dotenv(find_dotenv())

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_KEY_SECRET = os.environ.get("CONSUMER_KEY_SECRET")
MONGODB_URI = os.environ.get("MONGODB_URI")

class TweetStreamDBListener(StreamListener):
    ROOT_KEYS_TO_SAVE = ['created_at', 'id', 'text', 'geo', 'coordinates', \
    'place', 'retweet_count', 'favorite_count', 'entities', 'timestamp_ms']
    USER_KEYS_TO_SAVE = ['id', 'screen_name', 'location', 'verified', \
    'followers_count', 'time_zone', 'lang']

    def __init__(self, db):
        self.db = db

    def on_data(self, data):
        tweet_json = json.loads(data)

        data_to_save = {}
        for key in self.ROOT_KEYS_TO_SAVE:
            if key in tweet_json:
                data_to_save[key] = tweet_json[key]

        if 'user' in tweet_json:
            user = tweet_json['user']
            data_to_save['user'] = {}
            for key in self.USER_KEYS_TO_SAVE:
                if key in user:
                    data_to_save['user'][key] = user[key]

        if 'retweeted_status' in tweet_json or 'quoted_status' in tweet_json:
            data_to_save['is_retweet'] = True
        else:
            data_to_save['is_retweet'] = False

        self.db.insert(data_to_save)

        return True

    def on_error(self, status):
        print("\n\n")
        print(status)
        print("\n\n")


if __name__ == '__main__':
    print("💾  Connecting to database")
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    tweets = db.tweets

    #This handles Twitter authetification and the connection to Twitter Streaming API
    print("🔐  Authenticating with Twitter")
    listener = TweetStreamDBListener(tweets)
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    print("🌊  Starting tweet stream")
    stream = Stream(auth, listener)
    stream.filter(track=['#'])

    print("🌈  Done")
