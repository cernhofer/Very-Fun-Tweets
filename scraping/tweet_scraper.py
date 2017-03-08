import re
import bs4
import queue
import json
import sys
import csv
import pdb
import collections
import string
from collections import Counter
from nltk.corpus import wordnet as wn
import pandas as pd

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

#test is a list of tweet bodies

#scrape out

tweets_data_path = 'test_data.txt'

def scrape_tweet(word_string, word_list):
	for word in re.split('\\s+', word_string):
		if word != " " and word != "":
			word = word.lower()
			word = ''.join(x for x in word if x in string.printable)
			word = re.sub('[^a-zA-Z]+', '', word)
			if word not in INDEX_IGNORE:
				if not re.match(r'^#', word) and not re.match(r'^@', word) and not re.match(r'^https', word) and not re.match(r'^http', word) and word is not "" and word is not ' ':
						if word != '':
							word_list.append(word)

def run_for_your_life(hashtag_list):
	word_list = []
	num_tweets = len(hashtag_list)

	print("there are", num_tweets, "number of tweets in this hashtag!")


	for tweet_text in hashtag_list:
		scrape_tweet(tweet_text, word_list)

	c = Counter(word_list).most_common(3)
	test = list(c)

	print(test)

	common_words = []
	count = 0
	for word in common_words:
		count += word[1]
		common_words.append(word[0])

	if count/num_tweets > THRESH:
		print(common_words)
		return common_words

	else:
		return None






