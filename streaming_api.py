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

    def __init__(self, db):
        self.db = db

    def on_data(self, data):
        tweet_json = json.loads(data)
        keys_to_save = {
            'id': tweet_json['id'],
            'created_at': tweet_json['created_at'],
            'geo': tweet_json['geo'],
            'coordinates': tweet_json['coordinates'],
            'place': tweet_json['place'],
            'verified': tweet_json['user']['verified']
        }

        hashtags = tweet_json['entities']['hashtags']
        for hashtag in hashtags:
            record = self.db.tweets.find_one_and_update(
                {"hashtag": hashtag['text']},
                {'$push': {'tweets': keys_to_save}})

            if record is None:
                self.db.tweets.insert({
                    'hashtag': hashtag['text'],
                    'tweets': [keys_to_save]
                })
            print("\t", hashtag)

            # heroku run:detached python streaming_api.py

    def on_error(self, status):
        print("\n\n")
        print(status)
        print("\n\n")


if __name__ == '__main__':
    print("💾  Connecting to database")
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()

    #This handles Twitter authetification and the connection to Twitter Streaming API
    print("🔐  Authenticating with Twitter")
    listener = TweetStreamDBListener(db)
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    print("🌊  Starting tweet stream")
    stream = Stream(auth, listener)
    stream.filter(track=['#'])

    print("🌈  Done")
