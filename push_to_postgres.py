import json
import requests

def push_to_postgres(data):
    '''
    Create a session with Django app and post payload to the client
    '''
    REQUEST_BASE = 'http://www.veryfuntweets.com'
    REQUEST_PATH = 'tweet_search/populate'
    REQUEST_URL = '/'.join([REQUEST_BASE, REQUEST_PATH])

    client = requests.session()

    # retrieve the CSRF token
    client.get(REQUEST_URL)
    csrftoken = client.cookies['csrftoken']

    # create payload dictionary
    payload = dict(
    csrfmiddlewaretoken=csrftoken,
    payload=json.dumps(data)
    )

    # post payload to client
    response = client.post(REQUEST_URL, data=payload)
