import pandas as pd
import json
from datetime import datetime
prev_avg = 0

def extract_datetime(tweet):
    return datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")

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

def add_dates(start_date,increment):
    new_date = int(start_date[-2:]) + increment
    new_string = start_date[:-2] + str(new_date)
    return new_string

def get_tweetbuckets(counts_df):
    test = counts_df[['count','datestring']]
    tweetbuckets = []
    for index,row in test.iterrows():
        dictionary = pd.Series.to_dict(row)
        tweetbuckets.append(dictionary)
    return tweetbuckets

import pandas as pd
import json
from datetime import datetime
prev_avg = 0

def extract_datetime(tweet):
    return datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")

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

def get_tweetbuckets(counts_df):
    test = counts_df[['count','datestring']]
    tweetbuckets = []
    for index,row in test.iterrows():
        dictionary = pd.Series.to_dict(row)
        tweetbuckets.append(dictionary)
    return tweetbuckets

def spikes(sample_hashtag,threshold=0.2,spikes=3):
    df = pd.DataFrame.from_dict(sample_hashtag['tweets'])

    hashtag = sample_hashtag['hashtag']
    print("the hashtag is ",hashtag)

    df['datetime'] = df.apply (lambda row: extract_datetime(row),axis=1)
    df['datestring'] = df.apply (lambda row: datestring(row), axis=1 )
    counts = df['datestring'].value_counts()
    counts_df = pd.Series.to_frame(counts)
    counts_df['index'] = counts_df.index
    counts_df.columns = ['count','datestring']
    counts_df = counts_df.sort_values(by='datestring')

    counts_df = counts_df.reset_index()
    counts_df = counts_df.drop(['index'],axis = 1)
    counts_df['index'] = counts_df.index
    counts_df['n'] = counts_df.apply (lambda row: plus_one(row), axis=1 )
    prev_avg = 0
    counts_df['moving_average'] = counts_df.apply (lambda row: moving_average(row), axis=1 )
    counts_df['change'] = counts_df.apply (lambda row: change(row), axis=1 )
    counts_df = counts_df.sort_values(by='change',ascending=False)

    print(counts_df)
    has_spikes = []
    output={}
    spike_dates = []
    list_of_list_of_tweets = []
    for i in range(spikes):

        change1 = counts_df.iloc[i]['change']
        print(change1)
        if change1 >= threshold:
            # see if this one is a spike

            # update spike boolean
            has_spike = True
            # get spike date
            spike_date = counts_df.iloc[i]['datestring']
            # get list of tweets for this spike
            filtered_df = df.loc[df['datestring'] == spike_date[0]]
            tweet_text_list = filtered_df['tweet_text'].tolist()
            # append all results
            spike_dates.append(spike_date)
            has_spikes.append(has_spike)
            list_of_list_of_tweets.append(tweet_text_list)

    #print(has_spikes)
    #print(spike_dates)
    if len(has_spikes)>0:
        tweetbuckets = get_tweetbuckets(counts_df)
        output['hashtag'] = hashtag
        output['tweetbuckets'] = tweetbuckets

        return True, spike_dates, output, list_of_list_of_tweets

    return False, None, None, None


def insert_missing_data(start_date, end_date, counts_df):
    # index by date
    indexed_df = counts_df.set_index(['datestring'])
    start_value = indexed_df['count'][start_date]
    end_value = indexed_df['count'][end_date]
    num_days = int(end_date[-2:]) - int(start_date[-2:]) -1

    missing_dict = {}
    for i in range(num_days):
        key = add_dates(start_date,i+1)
        value = start_value + (end_value-start_value)/num_days
        start_value = value
        missing_dict[key]=value
    missing = pd.Series(missing_dict, name='count')
    missing.index.name = 'datestring'
    df = missing.to_frame()
    df = df.reset_index()

    new = counts_df.append(df, ignore_index=True)
    new = new.sort_values(by='datestring')
    return new
