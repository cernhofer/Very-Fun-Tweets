from django.db import models

class Hashtag(models.Model):
    name = models.CharField(max_length=140)

class TweetBucket(models.Model):
    timestamp = models.DateTimeField()
    count = models.IntegerField()
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    class Meta:
        ordering = ('timestamp',)

class Story(models.Model):
    timestamp = models.DateTimeField()
    url = models.URLField()
    headline = models.TextField()
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    class Meta:
        ordering = ('timestamp',)
