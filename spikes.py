import pandas as pd
import json
from datetime import datetime


tweets_data_path = 'reference_info/sample_data.txt'


def generate_tweets_df(tweets_data_path)
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    tweets = pd.DataFrame()
    tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
    return tweets


#test = pd.DataFrame.from_dict(sample_hashtag['tweets'])
# 2017-02-14 02:25:33
def extract_datetime(tweet):
    return datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")

def year(tweet):
    x = tweet['datetime']
    return str(x)[0:4]

def month(tweet):
    x = tweet['datetime']
    return str(x)[5:7]

def day(tweet):
    x = tweet['datetime']
    return str(x)[8:10]

def hour(tweet):
    x = tweet['datetime']
    return str(x)[11:13]

def minute(tweet):
    x = tweet['datetime']
    return str(x)[14:16]

def second(tweet):
    x = tweet['datetime']
    return str(x)[17:19]

def datestring(tweet):
    x = tweet['datetime']
    return str(x)[0:10]

def moving_average(row):
    global prev_avg
    alpha = 1/row['n']
    new_avg = (1-alpha)*prev_avg + alpha*row['count']
    prev_avg = new_avg
    return new_avg

def plus_one(row):
    return row['index'] +1

def change(row):
    val = row['count']
    avg = row['moving_average']
    return (val-avg)/avg

def spikes(sample_hashtag, threshold=0.2):
    df = pd.DataFrame.from_dict(sample_hashtag
                                ['tweets'])

    df['datetime'] = df.apply (lambda row: extract_datetime (row),axis=1)
    df['datestring'] = df.apply (lambda row: datestring(row), axis=1 )

    counts = df['datestring'].value_counts()
    counts_df = pd.Series.to_frame(counts)
    counts_df['index'] = counts_df.index
    counts_df.columns = ['count','datestring']
    counts_df = counts_df.reset_index()
    counts_df = counts_df.drop(['index'],axis = 1)
    counts_df['index'] = counts_df.index

    counts_df['n'] = counts_df.apply (lambda row: plus_one(row), axis=1 )
    prev_avg = 0
    counts_df['moving_average'] = counts_df.apply (lambda row: moving_average(row), axis=1 )
    counts_df['change'] = counts_df.apply (lambda row: change(row), axis=1 )

    max_row = counts_df.loc[counts_df['change'].idxmax()]
    max_change = max_row['change']
    max_date = max_row['datestring']
    spike_bool = False
    if max_change >= threshold:
        spike_bool = True
    return spike_bool, max_date, counts_df
