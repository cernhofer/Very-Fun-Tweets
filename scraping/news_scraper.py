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

'''
def get_query(input_query, ban_word):
	return_query = ''
	if len(input_query) > 1:
		for word in input_query:
			if return_query == '':
				return_query += word
			else:
				return_query += "+" + word
			if word in TWITTER_WORDS:
				#if one of the main words/hashtag is about twitter- don't take it out later
				ban_word = False
	else:
		return_query = input_query[0]

	return return_query
'''

def make_soup(url, **params):
	status_code = 503
	while status_code == 503:
		response = requests.get(url.format(**params), headers = HEADERS, verify=False)
		status_code = response.status_code

		if status_code == 503:
			print("Sleeping beauty time.")
			time.sleep(1800)

	return bs4.BeautifulSoup(response.text, "html5lib")

def get_news_url(div):
	urls = []
	for i in range(len(div)):
		for thing in div[i].find_all("a"):
			cleaned = re.search('(http)[^&]*', thing['href']).group()
			title =	thing.text

			urls.append([title, cleaned])

			print(title, cleaned)

	return urls

def get_string_from_list(list_tostring):
	final_string = ''
	for element in list_tostring:
		final_string += element + ' '

	return final_string

def get_article_text(link):
	link_text = ''
	link_soup = make_soup(link)
	p_tags = link_soup.find_all("p")
	if p_tags is None:
		return None

	for tag in p_tags:
		if tag.text is not None:
			link_text += tag.text

	if link_text == '':
		return None
	return link_text

def get_tf_matrix(tf_set):
	tf_idf_vectorizer = TfidfVectorizer()
	return tf_idf_vectorizer.fit_transform(tf_set)

def check_tf_idf(doc1, doc2, doc3, terms= TWITTER_WORDS):
    matrix = get_tf_matrix([terms, doc1, doc2, doc3])
    val = cosine_similarity(matrix[0:1], matrix)

    return val

def scrape_it_good(*args):
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
	print(dt_obj)
	month = str(dt_obj[6])
	e_date = dt_obj[8:10]
	s_date = int(e_date) - 1
	year = str(dt_obj[0:4])

	return year, month, s_date, e_date

def run_baby_run(hashtag, dt, common_words):
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



if __name__ == "__main__":
	run_baby_run('supergirl', ['2017-03-06', '2017-02-27'], [['alex', 'musical', 'episode'], ['alex', 'episode', 'supergirl']])
