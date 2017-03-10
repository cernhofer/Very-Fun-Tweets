from django.db import models
import html.parser as htmlparser

class Hashtag(models.Model):
    name = models.CharField(max_length=140)

class TweetBucket(models.Model):
    timestamp = models.DateTimeField()
    count = models.IntegerField()
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    def formatted_timestamp(self):
        return self.timestamp.strftime("%Y-%m-%d")

    class Meta:
        ordering = ('timestamp',)

class Story(models.Model):
    timestamp = models.DateTimeField()
    url = models.URLField()
    headline = models.TextField()
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    def formatted_timestamp(self):
        return self.timestamp.strftime("%Y-%m-%d")

    def clean_headline(self):
        cleaned = self.headline.replace("'", "")
        return cleaned

    class Meta:
        ordering = ('timestamp',)
