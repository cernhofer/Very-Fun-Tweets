from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader 
from django.http import Http404
import json


from tweet_search.models import Hashtag, TweetBucket, Story

def index(request):
	return render(request, 'tweet_search/index.html')

def results(request):
	search_term = request.GET.get('search_term')

	print("\n\n\n\n")
	print(search_term)

	print("\n\n\n\n")

	context = {
		'search_term': search_term,
	}

	return render(request, 'tweet_search/results.html', context)

def search(request):
	return render(request, 'tweet_search/search.html')


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
