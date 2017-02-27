import json
from django.shortcuts import render
from django.http import HttpResponse
from django.middleware import csrf

from tweet_search.models import Hashtag, TweetBucket, Story

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def populate(request):
    if request.method == 'GET':
        csfr.get_token(request)
        return HrrpResponse('ok')

    payload = json.loads(request.POST.get('payload'))

    # Delete any old data that exists
    hashtag = Hashtag(name=payload.get('hashtag'))
    hashtag.save()

    for tweetbucket in payload.get('tweetbuckets'):
        timestamp = tweetbucket.get('timestamp')
        count = tweetbucket.get('count')
        tb = TweetBucket(timestamp=timestamp, count=count, hashtag=hashtag)
        tb.save()

    for story in payload.get('stories'):
        timestamp = story.get('timestamp')
        url = story.get('url')
        s = Story(timestamp=timestamp, url=url, hashtag=hashtag)
        s.save()

    return HttpResponse('ok')
