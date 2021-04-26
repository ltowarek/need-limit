import datetime

from django.db import models


class Feed(models.Model):
    crawling_interval = models.DurationField(default=datetime.timedelta(hours=1))
    html_link = models.URLField(max_length=200)
    last_crawled = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    xml_link = models.URLField(max_length=200, unique=True)

    def __str__(self) -> str:
        return str(self.title)


class FeedEntry(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    link = models.URLField(max_length=200)
    published = models.DateTimeField()
    summary = models.TextField()
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "feed entries"

    def __str__(self) -> str:
        return str(self.title)
