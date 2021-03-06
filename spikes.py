null = ""
false = False
true = True

import pandas as pd
import json
from datetime import datetime
prev_avg = 0
prev_count = 0

def extract_datetime(tweet):
    '''
    Extracts datetime object from tweet object
    '''
    return datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")

def datestring(tweet):
    '''
    Extracts date string
    '''
    x = tweet['datetime']
    return str(x)[0:10]

def moving_average(row):
    '''
    Calculates moving average for each row
    '''
    global prev_avg
    alpha = 1/row['n']
    new_avg = (1-alpha)*prev_avg + alpha*row['count']
    prev_avg = new_avg
    return new_avg

def plus_one(row):
    '''
    Adds 1 to the index to create a column for 'n'-
    the number of days thus far. We didn't directly
    use the index because we sort the df and reset the
    index a couple of times
    '''
    return row['index'] +1

def add_dates(start_date,increment):
    '''
    Helper function to add dates within a single month
    '''
    new_date = int(start_date[-2:]) + increment
    new_string = start_date[:-2] + str(new_date)
    return new_string

def get_tweetbuckets(counts_df):
    '''
    Convert df to appropriate output format
    required to send to highcharts for plotting
    '''
    test = counts_df[['count','datestring']]
    tweetbuckets = []
    for index,row in test.iterrows():
        dictionary = pd.Series.to_dict(row)
        tweetbuckets.append(dictionary)
    return tweetbuckets

def change_avg(row):
    '''
    Compute change over moving average
    '''
    val = row['count']
    avg = row['moving_average']
    return (val-avg)/avg

def change_count(row):
    '''
    Compute change over prev day's count
    '''
    global prev_count
    if prev_count == 0:
        prev_count = 1
    current = row['count']
    day_change = (current - prev_count)/prev_count
    prev_count = current
    return day_change


def spikes(sample_hashtag,threshold=0.2,spikes=3):
    '''
    Take in a hashtag dictionary, a threshold and the number of
    spikes required and return
        boolean: whether or not there is a spikes
        spike_dates : list of dates on which spikes occurred
        output : dictionary required to plot graph
        list_of_list_of_tweets : tweet text needed for tweet scraper
    '''
    df = pd.DataFrame.from_dict(sample_hashtag['tweets'])

    hashtag = sample_hashtag['hashtag']

    df['datetime'] = df.apply (lambda row: extract_datetime(row),axis=1)
    df['datestring'] = df.apply (lambda row: datestring(row), axis=1 )
    counts = df['datestring'].value_counts()
    counts_df = pd.Series.to_frame(counts)
    counts_df['index'] = counts_df.index
    counts_df.columns = ['count','datestring']

    #sort the dataframe by date
    counts_df = counts_df.sort_values(by='datestring')
    counts_df = counts_df.reset_index()
    counts_df = counts_df.drop(['index'],axis = 1)
    counts_df['index'] = counts_df.index
    prev_count = counts_df.iloc[0]['count']
    counts_df['change_prev'] = counts_df.apply (lambda row: change_count(row), axis=1 )
    counts_df['n'] = counts_df.apply (lambda row: plus_one(row), axis=1 )
    prev_avg = 0
    counts_df['moving_average'] = counts_df.apply (lambda row: moving_average(row), axis=1 )
    counts_df['change'] = counts_df.apply (lambda row: change_avg(row), axis=1 )
    counts_df = counts_df.sort_values(by='change',ascending=False)

    has_spikes = []
    output={}
    spike_dates = []
    list_of_list_of_tweets = []
    for i in range(spikes):
        change1 = counts_df.iloc[i]['change']
        change2 = counts_df.iloc[i]['change_prev']

        if change1 >= threshold and change2 >= threshold*2:
            has_spike = True
            spike_date = counts_df.iloc[i]['datestring']
            filtered_df = df.loc[df['datestring'] == spike_date]
            tweet_text_list = filtered_df['tweet_text'].tolist()
            spike_dates.append(spike_date)
            has_spikes.append(has_spike)
            list_of_list_of_tweets.append(tweet_text_list)

    if len(has_spikes)>0:
        tweetbuckets = get_tweetbuckets(counts_df)
        output['hashtag'] = hashtag
        output['tweetbuckets'] = tweetbuckets

        return True, spike_dates, output, list_of_list_of_tweets

    return False, None, None, None


def insert_missing_data(start_date, end_date, counts_df):
    '''
    Helper function to plug in values for dates on which
    RCC was down - ultimately, highcharts handles this issue
    '''
    # index by date
    indexed_df = counts_df.set_index(['datestring'])
    start_value = int(indexed_df['count'][start_date])
    end_value = int(indexed_df['count'][end_date])
    num_days = int(end_date[-2:]) - int(start_date[-2:])

    missing_dict = {}
    for i in range(num_days):
        key = add_dates(start_date,i+1)
        value = start_value + (end_value-start_value)/num_days
        start_value = value
        missing_dict[key]=value
        counts_df = counts_df[counts_df['datestring'] != str(key)]

    missing = pd.Series(missing_dict, name='count')
    missing.index.name = 'datestring'
    df = missing.to_frame()
    df = df.reset_index()

    new = counts_df.append(df, ignore_index=True)
    new = new.sort_values(by='datestring')
    return new
