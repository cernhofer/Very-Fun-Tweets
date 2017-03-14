import os
import requests
import bs4
import html5lib
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import time


URL = 'https://www.google.com/search?cf=all&hl=en&pz=1&ned=en_ph&tbm=nws&gl=ph&as_q={query}&as_occt=any&as_drrb=b&as_mindate={month}%2F{start_date}%2F{year}&as_maxdate={month}%2F{end_date}%2F{year}&tbs=cdr%3A1%2Ccd_min%3A{month}%2F{start_date}%2F{year}%2Ccd_max%3A{month}%2F{end_date}%2F{year}&authuser=0'
TWITTER_WORDS = 'twitter hashtag trending tweeted tweet'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}


def make_soup(url, **params):
	'''
	Takes in URL and parameters for string interpolation. Return bs4 object. Sleeps
	for a little bit every time a query is made and when 503 error is thrown. 
	'''
	status_code = 503
	while status_code == 503:
		response = requests.get(url.format(**params), headers = HEADERS, verify=False)
		status_code = response.status_code

		if status_code == 503:
			time.sleep(1800)
		else:
			time.sleep(300)

	return bs4.BeautifulSoup(response.text, "html5lib")

def get_news_url(div):
	'''
	Takes in div from google news, parses through and finds all a tags. Returns 
	title of article found and cleaned URL. 
	'''
	urls = []
	for i in range(len(div)):
		for thing in div[i].find_all("a"):
			cleaned = re.search('(http)[^&]*', thing['href']).group()
			title =	thing.text

			urls.append([title, cleaned])

			print(title, cleaned)

	return urls

def get_string_from_list(list_tostring):
	'''
	Takes in a list and returns a string of elements in the list, separated
	by a space. 
	'''
	final_string = ''
	for element in list_tostring:
		final_string += element + ' '

	return final_string

def get_article_text(link):
	'''
	Gets and returns article text from p-tags in link provided. If any element 
	on the webpage isn't found or is None, returns None. 
	'''
	try:
		link_text = ''
		link_soup = make_soup(link)
		p_tags = link_soup.find_all("p")
		if p_tags is None:
			return None

		for tag in p_tags:
			if tag.text:
				link_text += tag.text

		if link_text == '':
			return None

		return link_text
	except:
		return None

def get_tf_matrix(tf_set):
	'''
	Creates Tfidf vector object, vectorizes set passed in 
	'''
	tf_idf_vectorizer = TfidfVectorizer()
	return tf_idf_vectorizer.fit_transform(tf_set)

def check_tf_idf(doc1, doc2, doc3, terms= TWITTER_WORDS):
	'''
	creates Tfidf matrix, finds and returns matrix of cosine values
	'''
    matrix = get_tf_matrix([terms, doc1, doc2, doc3])
    val = cosine_similarity(matrix[0:1], matrix)

    return val

def scrape_it_good(*args):
	'''
	Takes in parameters for URL string interpolation and common words as parameters.
	Gets soup object, parses through relevant article texts. With tf_idf values, finds
	most applicable and least 'twitter obessed' article and return its title and URL. 
	'''
	ban_twitter = True
	hashtag, common_words, month, start_date, end_date, year = args
	soup = make_soup(URL, query=hashtag, month=month, start_date=start_date, end_date=end_date, year=year)
	divs = soup.find_all("div", class_ = "_cnc")
	divs += soup.find_all("div", class_ = "_hnc card-section")
	news_links = get_news_url(divs)


	print(len(news_links))
	if len(news_links) < 3:
		print("NOT ENOUGH NEWS ARTICLES")
		return None, None

	final_list = []

	text1 = get_article_text(news_links[0][1])
	text2 = get_article_text(news_links[1][1])
	text3 = get_article_text(news_links[2][1])

	if text1 is None or text2 is None or text3 is None:
		return None, None

	key_words_val = check_tf_idf(text1, text2, text3, get_string_from_list(common_words))

	if ban_twitter:
		twitter_val = check_tf_idf(text1, text2, text3)

	for i in range(len(key_words_val[0])):
		if i != 0:
			if ban_twitter:
				if twitter_val[0][i] < 0.025:
					#it's good and we can keep it on the list
					final_list.append(news_links[i-1] + [key_words_val[0][i]])
			else:
				final_list.append(news_links[i-1] + [key_words_val[0][i]])

	final_list.sort(key=lambda x: x[2], reverse= True)

	return final_list[0][0], final_list[0][1]

def get_date(dt_obj):
	'''
	Parses through date string to get individual values of month, date, year.
	THIS SUCKS I KNOW. Don't hate. 
	'''
	print(dt_obj)
	month = str(dt_obj[6])
	e_date = dt_obj[8:10]
	s_date = int(e_date) - 1
	year = str(dt_obj[0:4])

	return year, month, s_date, e_date

def run_baby_run(hashtag, dt, common_words):
	'''
	Runs the baby! Main function called from the outside world.  Takes in hashtag,
	datestring, and common_words list. Calls scrape_it_good for each date and list
	of common words. Returns formatted dictionary ready to be put in a database! 
	'''
	to_return = []

	for i, date in enumerate(dt):
		if common_words[i] == None:
			print("common words was empty")
			continue
		year, month, start, end = get_date(date)  #don't know if this will work!!!
		args_to_pass = (hashtag, common_words[i], month, start, end, year)
		title, url = scrape_it_good(*args_to_pass)
		if title is None:
			continue
		story_dict = {'timestamp': date, 'url': url, 'headline': title}
		to_return.append(story_dict)

	if to_return == []:
		print("No news worthy data from any of the days!!!")
		return None
	else:
		print("\n\nNEWS ARTICLE:", to_return)
		return to_return

