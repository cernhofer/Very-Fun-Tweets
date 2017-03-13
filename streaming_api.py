import os, json
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

# Variables that contains the user credentials to access Twitter API
load_dotenv(find_dotenv())
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_KEY_SECRET = os.environ.get("CONSUMER_KEY_SECRET")
MONGODB_URI = os.environ.get("MONGODB_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

class TweetStreamDBListener(StreamListener):
    '''
    This class inherits StreamListener from Tweepy and cleans and sends data
    to the MongoDB and reports errors.
    '''

    def __init__(self, db):
        self.db = db

    def on_data(self, data):
        '''
        When a tweet is detected by the StreamListener, clean the data and send
        it to the MongoDB
        '''
        try:
            tweet_json = json.loads(data)
            # stipulate which keys have information we want in the MongoDB
            keys_to_save = {
                'id': tweet_json['id'],
                'created_at': tweet_json['created_at'],
                'tweet_text': tweet_json['text'],
                'geo': tweet_json['geo'],
                'coordinates': tweet_json['coordinates'],
                'place': tweet_json['place'],
                'verified': tweet_json['user']['verified']
            }

            # collect all the hashtags in the tweet and assign all wanted
            # information to the new object created
            hashtags = tweet_json['entities']['hashtags']
            for hashtag in hashtags:
                lower_hashtag = hashtag['text'].lower()
                keys_to_save['orig_hashtag'] = hashtag['text']

                # if hashtag already exists in databse, just push new data into
                # it
                record = self.db.tweets.find_one_and_update(
                    {'hashtag': lower_hashtag},
                    {'$push': {'tweets': keys_to_save}})

                # if hashtag does not already exist, insert it and the data into
                # the MongoDB
                if record is None:
                    self.db.tweets.insert({
                        'hashtag': lower_hashtag,
                        'tweets': [keys_to_save]
                    })
        except:
            pass

    def on_error(self, status):
        print("\n\n")
        print(status)
        print("\n\n")


if __name__ == '__main__':
    while True:
        try:
            print("💾  Connecting to database")

            client = MongoClient(MONGODB_URI)

            # the first works if running on Heroku, the second if running on RCC
            if DATABASE_NAME is None:
                db = client.get_default_database()
            else:
                db = client[DATABASE_NAME]

            # Handling Twitter authetification and the connection to Twitter
            # Streaming API
            print("🔐  Authenticating with Twitter")
            listener = TweetStreamDBListener(db)
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

            # create stream object and begin streaming the sample
            print("🌊  Starting tweet stream")
            stream = Stream(auth, listener)
            stream.sample(languages=['en'])

            print("🌈  Done")

        except:
            print("⛑  An exception occurred!")
