import oauth2 as oauth
import json

search_api = 'https://api.twitter.com/1.1/search/tweets.json?q=%23womensmarch'

token_key = '30073662-UdrywPW0DZ0KoTeEpkEbfr9Eo84YXhLZ9CMuxX7Jo'
token_secret = 'Hkx8GIZnkzYnGgdo39JmkEdrUqrlrc24CaKG7RUJVQm5J'

consumer_key = 'r0CvQ8ZrEHDUo6deY3DWxnQGc'
consumer_secret = '8j3jhVLlBqmJLX2Cg6AXZZCM9MzNwJN3dYh6qQkMoMNoeUaYvk'

def oauth_req(url, token_key, token_secret, consumer_key, consumer_secret, http_method="GET"):
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(key=token_key, secret=token_secret)
    client = oauth.Client(consumer, token)
    resp, content = client.request(url, method=http_method)
    return resp, content

resp, content = oauth_req(search_api, token_key, token_secret, consumer_key, consumer_secret)

str_response = content.decode('utf-8')
tweets = json.loads(str_response)

# tweets is a dictionary with two keys: statuses and search_metadata
# all pertinent info will be found in statuses

num_tweets = 0

for tweet in tweets['statuses']:
    print(tweet, '\n\n')
    num_tweets += 1

print(num_tweets)
