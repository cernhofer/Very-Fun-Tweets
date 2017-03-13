from tweet_search.models import Hashtag, Story, TweetBucket

for hashtag in Hashtag.objects.all():
  print(h.name)

Hashtag.objects.count()
