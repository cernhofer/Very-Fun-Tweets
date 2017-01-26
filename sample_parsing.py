import json
import pandas as pd
import matplotlib.pyplot as plt

tweets_data_path = "sample_data.txt"

count = 0
tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
        count += 1
    except:
        continue

print(count)
