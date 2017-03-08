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

def spikes(sample_hashtag,tolerance=0.2,spikes=1):
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

    has_spike = False
    spike_index = counts_df['change'].idxmax(axis=0, skipna=True)
    change_d = counts_df.iloc[spike_index]['change']

    print("the highest change is",     change_d)

    if change_d >= 0.2:
        has_spike = True
    print("has_spike = ", has_spike)
    spike_date = ""
    output={}

    #if push_to_chelsea:
    if has_spike:
        tweetbuckets = get_tweetbuckets(counts_df)
        output['hashtag'] = hashtag
        output['tweetbuckets'] = tweetbuckets
        spike_date = [counts_df.iloc[spike_index]['datestring']]
        filtered_df = df.loc[df['datestring'] == spike_date]
        tweet_text_list = filtered_df['tweet_text'].tolist()

    return has_spike, spike_date, output, tweet_text_list
