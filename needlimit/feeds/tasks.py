import feeds.services as services
from celery import shared_task
from feeds.models import Feed


@shared_task
def crawl_feeds() -> None:
    feeds = Feed.objects.all()
    for feed in feeds:
        crawl_feed.delay(feed.id)


@shared_task
def crawl_feed(feed_id: int) -> None:
    services.crawl_feed_by_id(feed_id)
