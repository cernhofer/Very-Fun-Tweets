import os
import requests
import bs4
import html5lib
import re

URL = 'https://www.google.com/search?cf=all&hl=en&pz=1&ned=en_ph&tbm=nws&gl=ph&as_q={query}%20&as_occt=any&as_drrb=b&as_mindate={month}%2F{start_date}%2F{year}&as_maxdate={month}%2F{end_date}%2F{year}&tbs=cdr%3A1%2Ccd_min%3A{month}%2F{start_date}%2F{year}%2Ccd_max%3A{month}%2F{end_date}%2F{year}&authuser=0'

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

def get_article_text(link, news_dict):
	link_text = ''
	link_soup = make_soup(link)
	p_tags = link_soup.find_all("p")
	for tag in p_tags:
		link_text += tag.text
	news_dict[link] = link_text

if __name__ == "__main__":
	in_query = ['trump', 'ban', 'judge']

	query = get_query(in_query)
	month = 2
	start_date = 7
	end_date = 8
	year = 2017

	soup = make_soup(URL, query=query, month=2, start_date=7, end_date=7, year=2017)

	divs = soup.find_all("div", id = "center_col")

	news_links = get_news_url(divs)

	news_dict = {}

	for link in news_links:
		print(link,'\n')
		get_article_text(link, news_dict)


	for key, thing in news_dict.items():
		print(key,thing)











