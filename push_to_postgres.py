import json
import requests

def push_to_postgres(data):
    REQUEST_BASE = 'http://localhost:8000' # change to be heroku app base url
    REQUEST_PATH = 'tweet_search/populate'
    REQUEST_URL = '/'.join(REQUEST_BASE, REQUEST_PATH)

    client = requests.session()

    # retrieve the CSRF token first
    client.get(REQUEST_URL)
    csrftoken = client.cookies['csrftoken']

    payload = dict(
    csrfmiddlewaretoken=csrftoken,
    payload=json.dumps(data)
    )

    response = client.post(REQUEST_URL, data=payload)


##### FOR TESTING
import datetime as dt
data = {
    'hashtag': 'goat',
    'tweetbuckets': [
        {
            'timestamp': (dt.datetime.today() - dt.timedelta(days=3, hours=1)).isoformat(),
            'count': 10,
        },
        {
            'timestamp': (dt.datetime.today() - dt.timedelta(days=3, hours=2)).isoformat(),
            'count': 20,
        },
        {
            'timestamp': (dt.datetime.today() - dt.timedelta(days=3, hours=3)).isoformat(),
            'count': 5,
        }
    ],
    'stories': [
        {
            'timestamp': (dt.datetime.today() - dt.timedelta(days=3, hours=2)).isoformat(),
            'url': 'https://google.com',
        }
    ],
}

push_to_postgres(data)
