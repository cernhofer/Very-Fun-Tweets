import os
import requests
import bs4
import html5lib
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

URL = 'https://www.google.com/search?cf=all&hl=en&pz=1&ned=en_ph&tbm=nws&gl=ph&as_q={query}%20&as_occt=any&as_drrb=b&as_mindate={month}%2F{start_date}%2F{year}&as_maxdate={month}%2F{end_date}%2F{year}&tbs=cdr%3A1%2Ccd_min%3A{month}%2F{start_date}%2F{year}%2Ccd_max%3A{month}%2F{end_date}%2F{year}&authuser=0'
TWITTER_WORDS = 'twitter hashtag trending'


def get_query(input_query):
	return_query = ''
	if len(input_query) > 1:
		for word in input_query:
			if return_query == '':
				return_query += word
			else:
				return_query += "+" + word
	else:
		return_query = input_query[0]

	return return_query
		

def make_soup(url, **params):
	response = requests.get(url.format(**params))
	return bs4.BeautifulSoup(response.text, "html5lib")

def get_news_url(div):
	urls = set()
	for thing in div[0].find_all("a"):
		cleaned = re.search('(http)[^&]*', thing['href']).group()

		urls.add(cleaned)

	return urls

def get_article_text(link):
	link_text = ''
	link_soup = make_soup(link)
	p_tags = link_soup.find_all("p")
	for tag in p_tags:
		link_text += tag.text

	return link_text

def get_tf_idf(tf_set):
	tf_idf_vectorizer = TfidfVectorizer()
	return tf_idf_vectorizer.fit_transform(tf_set)


def scrape_it_good(key_words, *args):
	'''
	in_query = ['trump', 'ban', 'judge']

	query = get_query(in_query)
	month = 2
	start_date = 7
	end_date = 8
	year = 2017
	'''
	in_query, month, start_date, end_date, year = args
	query = get_query(in_query)

	soup = make_soup(URL, query=query, month=2, start_date=7, end_date=7, year=2017)

	divs = soup.find_all("div", id = "center_col")

	news_links = get_news_url(divs)

	news_dict = {}

	for link in news_links:
		text = get_article_text(link)

		twitter_matrix = get_tf_idf([TWITTER_WORDS, text])

		key_word_matrix = get_tf_idf([key_words, text])

		twitter_val = cosine_similarity(twitter_matrix[0:1], twitter_matrix)[0][1]

		key_word_val = cosine_similarity(key_word_matrix[0:1], key_word_matrix)[0][1]

		if twitter_val < 0.15:
			print(link, 'IS GOOD')
			news_dict[link] = key_word_val

	sorted(news_dict.items(), key=lambda x: x[1])

	news_list = list(news_dict)

	print(news_list[:3])

if __name__ == "__main__":
	args_to_pass = (['trump', 'ban', 'judge'], 2, 7, 8, 2017)
	scrape_it_good('ban trump judge', *args_to_pass)


