import os, json
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from matplotlib import dates as mdates, pyplot
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

load_dotenv(find_dotenv())
MONGODB_URI = os.environ.get("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

# find a hashtag with more than some number of tweets
hashtag = db.tweets.find_one({'tweets.1700': {'$exists':True}})
hashtag_text = hashtag['hashtag']

list_of_tweets = hashtag['tweets']

# searching for one hashtag in particular
    # search = {'hashtag':'ig'}
    # results = db.tweets.find(search)
    # list_of_tweets = results[0]['tweets']

created_datetimes = []
for tweet in list_of_tweets:
    date = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.timezone('US/Central'))
    created_datetimes.append(date)

dates = mdates.date2num(created_datetimes)

# simple plot with nonsense y-axis, possible rate of tweets with slope
    # values = list(range(len(created_datetimes)))
    # plt.plot_date(dates, values, ls='solid')
    # plt.show()

# bin the dates into some number of hours and plot hist
fig, ax = plt.subplots()
ax.hist(dates, color='#6BA4B0', edgecolor='k' )
ax.set_title('Histogram of #%s Usage' % hashtag_text)
ax.set_xlabel('Time of tweet using #%s' % hashtag_text)
locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
plt.show()
