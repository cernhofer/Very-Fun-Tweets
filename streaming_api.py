from pymongo import MongoClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from dotenv import load_dotenv, find_dotenv
import os
import pdb

load_dotenv(find_dotenv())

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_KEY_SECRET = os.environ.get("CONSUMER_KEY_SECRET")
MONGODB_URI = os.environ.get("MONGODB_URI")

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    client = MongoClient(MONGODB_URI)

    db = client.get_default_database()

    tweets = db.tweets 
    
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)

    '''

    created_at 
    id
    text
    user
        id
        screen_name 
        location 
        verified 
        followers_count 
        time_zone 
        lang 
    geo 
    coordinates 
    place 
    retweet 
    retweeted status? 
    entities
        hashtags 
        urls
        user_mentions
        symbols 
    timestamp_ms 
    retweet_count
    favourite_count


    '''
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['#'])

    print("DONE")










