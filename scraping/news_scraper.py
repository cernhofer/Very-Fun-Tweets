import os
import requests
import bs4
import html5lib
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


URL = 'https://www.google.com/search?cf=all&hl=en&pz=1&ned=en_ph&tbm=nws&gl=ph&as_q={query}&as_occt=any&as_drrb=b&as_mindate={month}%2F{start_date}%2F{year}&as_maxdate={month}%2F{end_date}%2F{year}&tbs=cdr%3A1%2Ccd_min%3A{month}%2F{start_date}%2F{year}%2Ccd_max%3A{month}%2F{end_date}%2F{year}&authuser=0'
TWITTER_WORDS = 'twitter hashtag trending tweeted tweet'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}


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
	response = requests.get(url.format(**params), headers = HEADERS)
	return bs4.BeautifulSoup(response.text, "html5lib")

def get_news_url(div):
	urls = []
	for i in range(len(div)):
		for thing in div[i].find_all("a"):
			cleaned = re.search('(http)[^&]*', thing['href']).group()
			title =	thing.text

			urls.append((title, cleaned))

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

def scrape_it_good(*args):
	in_query, month, start_date, end_date, year = args
	query = get_query(in_query)
	soup = make_soup(URL, query=query, month=month, start_date=start_date, end_date=end_date, year=year)
	divs = soup.find_all("div", class_ = "_cnc")
	divs += soup.find_all("div", class_ = "_hnc card-section")
	news_links = get_news_url(divs)

	twitter_matrix = get_tf_idf([TWITTER_WORDS, get_article_text(news_links[0][1]), get_article_text(news_links[1][1]), get_article_text(news_links[2][1]), get_article_text(news_links[3][1]), get_article_text(news_links[4][1])])

	twitter_val = cosine_similarity(twitter_matrix[0:1], twitter_matrix)

	final_list = []
	for i in range(len(twitter_val[0])):
		if i != 0:
			if twitter_val[0][i] < 0.025:
				#it's good and we can keep it on the list
				final_list.append(news_links[i-1])

	return final_list[0][0], final_list[0][1]

def get_date(dt_obj):
	print(dt_obj)
	month = str(dt_obj[6])
	e_date = dt_obj[8:10]
	s_date = int(e_date) - 1
	year = str(dt_obj[0:4])

	return year, month, s_date, e_date

def run_baby_run(hashtag, dt, common_words):
	#to_return = list of dictionaries!!!!!!!!!
	to_return = []

	for i, date in enumerate(dt):
		year, month, start, end = get_date(date)  #don't know if this will work!!!
		search_words = [hashtag] + common_words
		args_to_pass = (search_words, month, start, end, year)
		title, url = scrape_it_good(*args_to_pass)
		story_dict = {'timstamp': date, 'url': url, 'healine': title}
		to_return.append(story_dict)

	print(to_return)
	return to_return
