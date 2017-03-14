import re
#import bs4
import json
import sys
import csv
import pdb
import collections
import string
from collections import Counter

THRESH = 0.4

INDEX_IGNORE = set(['a',  'also',  'an',  'and',  'are', 'as',  'at',  'be', 'was',
                    'but',  'by',  'course',  'for',  'from',  'how', 'i', 'you',
                    'ii',  'iii',  'in',  'include',  'is',  'not',  'of', 'not', 'no',
                    'on',  'or',  's',  'so', 'it', 'there', 'but', 'by', 'I', 'me',
                    'such',  'that',  'the',  'their',  'this',  'through',  'to',
                    'we', 'were', 'which', 'will', 'with', 'yet', 'rt', 'mr', 'he', 'your', 
                    'this', 'its', 'about', 'his', 'her', 'our', 'all', 'out', 'if', 'my', 
                    'up', 'us', 'have', 'like', 'when', 'rt', 'go', 'they', 'who', 'do'
                    'just', 'can', 'do', 'dont', 'im', 'she', 'did', 'got', 'today'])


def scrape_tweet(word_string, word_list, hashtag):
	'''
	Takes in a string of words, creates a list of words that meet certain 
	criteria. Returns nothing but updates word_list. 
	'''
	for word in re.split('\\s+', word_string):
		if word != " " and word != "":
			word = word.lower()
			word = ''.join(x for x in word if x in string.printable)
			word = re.sub('[^a-zA-Z]+', '', word)
			if word not in INDEX_IGNORE:
				if not re.match(r'^#', word) and not re.match(r'^@', word) and not re.match(r'^https', word) and not re.match(r'^http', word) and word is not "" and word is not ' ':
						if word != hashtag:
							word_list.append(word)

def run_for_your_life(hashtag_list, hashtag):
	'''
	Main function called by outside world. Takes in list of tweet text lists.
	Parses through list, uses Counter object to find 3 most used words, if even 
	one group of words (from the list) meets criteria, pass back all lists of
	common words. 
	'''
	return_words = False
	common_words_list = []
	for i, indiv_list in enumerate(hashtag_list):

		all_words = []
		print(len(indiv_list))
		num_tweets = len(indiv_list)

		for tweet_text in indiv_list:
			scrape_tweet(tweet_text, all_words, hashtag)

		c = Counter(all_words).most_common(3)

		word_list = list(c)

		common_words = []
		count = 0
		for word in word_list:
			count += word[1]
			common_words.append(word[0])

		if count/float(num_tweets) > THRESH:
			return_words = True

		common_words_list.append(common_words)

	if return_words:
		return common_words_list
	else:
		return None

















