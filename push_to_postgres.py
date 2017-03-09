import json
import requests

def push_to_postgres(data):
    REQUEST_BASE = 'http://www.veryfuntweets.com'
    REQUEST_PATH = 'tweet_search/populate'
    REQUEST_URL = '/'.join([REQUEST_BASE, REQUEST_PATH])

    client = requests.session()

    # retrieve the CSRF token first
    client.get(REQUEST_URL)

    csrftoken = client.cookies['csrftoken']

    payload = dict(
    csrfmiddlewaretoken=csrftoken,
    payload=json.dumps(data)
    )

    response = client.post(REQUEST_URL, data=payload)
