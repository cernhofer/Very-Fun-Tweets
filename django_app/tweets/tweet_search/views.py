from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader 
from django.http import Http404


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

  
