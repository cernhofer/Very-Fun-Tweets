from push_to_postgres import push_to_postgres
from scraping.news_scraper import * # find out name of function

hashtags = db.tweets.all()
for hashtag in hashtags:
    if len(hashtag.tweets) < 1000: continue

    has_spike, spike_data = sush_script(hashtag) # returns bool

    if has_spike:
        # data = prepare_data(hashtag) # outputs a formatted data object
        spike_data['stories'] = chelsea_script(hashtag) # or pass the spike data
        push_to_postgres(data)
    elif is_in_list(hashtag):
        # have this push to postgres if hashtag is on list of previously pushed hashtags
        # no need to call chelsea_script, need to handle for no stories bc postgres?
        push_to_postgres(data)


def is_in_list(hashtag):
    # create a list to be stored in mongo and check if hashtag is in there
    # returns bool

def add_to_list(hashtag):
    # write this
