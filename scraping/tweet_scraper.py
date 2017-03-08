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

TEST = ["#HowToDealWithAnEx get a puppy. \n\nThere, how easy was that?", "RT @therealjuicyj: #HowToDealWithAnEx  pull at the RBBTOUR &amp; get HOTBOXED", "#HowToDealWithAnEx I wouldn't know. All of mine have mysteriously disappeared.", "#HowToDealWithAnEx just leave it near the end of the alphabet - where it belongs.", "#HowToDealWithAnEx Adopt a cat and receive true love. https:\/\/t.co\/IfdN87Mp5e", "#HowToDealWithAnEx O.J. Simpson \ud83d\ude02\ud83d\ude37", "#HowToDealWithAnEx\n\nJust.Fucking.Don't", "When someone mentions my ex... #HowToDealWithAnEx https:\/\/t.co\/pjPxTE3Ums", "#HowToDealWithAnEx\n\nLive a happy, successful life.."]

test = ["WASHINGTON — President Trump on Monday signed a revised version of his executive order that would for the first time rewrite American immigration policy to bar migrants from predominantly Muslim nations, removing citizens of Iraq from the original travel embargo and scrapping a provision that explicitly protected religious minorities. The order, which comes about a month after federal judges blocked Mr. Trump’s haphazardly executed ban in January on residents from seven Middle Eastern and African countries, will not affect people who had previously been issued visas — a change that the administration hopes will avoid the chaos, protests and legal challenges that followed the first order. But it did little to halt criticism from Democrats and immigrant rights groups, which predicted a renewed fight in the courts. Mr. Trump’s initial, hastily issued order on Jan. 27 prompted protests across the country, leaving tearful families stranded at airports abroad and in the United States. The new measure will be phased in over the next two weeks, according to officials with the Department of Homeland Security.Continue reading the main story John F. Kelly, the Homeland Security secretary, said the order was “prospective” and applied “only to foreign nationals outside of the United States” who do not have a valid visa. “If you have a current valid visa to travel, we welcome you,” said Mr. Kelly, appearing alongside Secretary of State Rex W. Tillerson and Attorney General Jeff Sessions at the Ronald Reagan Federal Building in Washington early Monday — before leaving without taking reporters’ questions. “Unregulated, unvetted travel is not a universal privilege, especially when national security is at stake,” Mr. Kelly added. The indefinite ban on refugees from Syria also has been reduced to a 120-day ban, requiring review and renewal."]

INDEX_IGNORE = set(['a',  'also',  'an',  'and',  'are', 'as',  'at',  'be', 'was',
                    'but',  'by',  'course',  'for',  'from',  'how', 'i', 'you',
                    'ii',  'iii',  'in',  'include',  'is',  'not',  'of', 'not', 'no',
                    'on',  'or',  's',  'so', 'it', 'there', 'but', 'by', 'I', 'me',
                    'such',  'that',  'the',  'their',  'this',  'through',  'to',
                    'we', 'were', 'which', 'will', 'with', 'yet', 'rt', 'mr', 'he', 'your', 
                    'this', 'its', 'about'])

#test is a list of tweet bodies

#scrape out

tweets_data_path = 'test_data.txt'

def scrape_tweet(word_string, word_list):
	for word in re.split('\\s+', word_string):
		if word != " " and word != "":
			word = word.lower()
			word = ''.join(x for x in word if x in string.printable)
			if word not in INDEX_IGNORE:
				if not re.match(r'^#', word) and not re.match(r'^@', word) and not re.match(r'^https', word) and not re.match(r'^http', word) and word is not "" and word is not ' ':
						word_toadd = re.sub('[^a-zA-Z]+', '', word)
						if word_toadd != '':
							word_list.append(word_toadd)

def run_for_your_life(hashtag_list):
	word_list = []
	num_tweets = len(hashtag_list)

	print("there are", num_tweets, "number of tweets in this hashtag!")


	for tweet_text in hashtag_list:
		scrape_tweet(tweet_text, word_list)

	c = Counter(word_list).most_common(3)
	test = list(c)

	print(test)

	to_return = []
	for thing in test:
		to_return.append(thing[0])

	print(to_return)
	return to_return
