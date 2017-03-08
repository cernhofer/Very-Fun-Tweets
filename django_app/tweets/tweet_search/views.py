from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.middleware import csrf
import json
from django.core.exceptions import ObjectDoesNotExist
from tweet_search.models import Hashtag, TweetBucket, Story

def index(request):
	return render(request, 'tweet_search/index.html')

def results(request):
	search_term = request.GET.get('search_term')

	hashtag_data = None
	try:
		hashtag_data = Hashtag.objects.get(name=search_term)
	except ObjectDoesNotExist:
		pass

	context = {
		'search_term': search_term,
		'hashtag_data': hashtag_data,
	}

	return render(request, 'tweet_search/results.html', context)

def search(request):
	return render(request, 'tweet_search/search.html')


def populate(request):
	if request.method == 'GET':
		csrf.get_token(request)
		return HttpResponse('ok')

	payload = json.loads(request.POST.get('payload'))

	# Delete any old data that exists
	hashtag_in_db = Hashtag.objects.filter(name=payload.get('hashtag'))
	hashtag_in_db.all().delete()

	hashtag = Hashtag(name=payload.get('hashtag'))
	hashtag.save()

	for tweetbucket in payload.get('tweetbuckets'):
		timestamp = tweetbucket.get('datestring')
		count = tweetbucket.get('count')
		tb = TweetBucket(timestamp=timestamp, count=count, hashtag=hashtag)
		tb.save()

	for story in payload.get('stories'):
		timestamp = story.get('timestamp')
		url = story.get('url')
		headline = story.get('headline')
		s = Story(timestamp=timestamp, url=url, hashtag=hashtag, headline=headline)
		s.save()

	return HttpResponse('ok')
