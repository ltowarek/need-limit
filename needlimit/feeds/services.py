import datetime

import feedparser
from django.utils.timezone import make_aware
from feeds.models import Feed, FeedEntry


def crawl_feed_by_id(feed_id: int) -> None:
    feed = Feed.objects.get(id=feed_id)
    crawl_feed(feed)


def crawl_feed(feed: Feed) -> None:
    parsed_feed = feedparser.parse(feed.xml_link)
    feed = import_feed(parsed_feed)
    crawl_feed_entries(feed, parsed_feed.entries)


def import_feed(parsed_feed: feedparser.FeedParserDict) -> Feed:
    feed, _ = Feed.objects.update_or_create(
        xml_link=parsed_feed.href,
        defaults={
            "title": parsed_feed.feed.title,
            "html_link": parsed_feed.feed.link,
        },
    )
    return feed


def crawl_feed_entries(
    feed: Feed, parsed_entries: list[feedparser.FeedParserDict]
) -> None:
    for parsed_entry in parsed_entries:
        import_feed_entry(feed, parsed_entry)


def import_feed_entry(feed: Feed, parsed_entry: feedparser.FeedParserDict) -> FeedEntry:
    entry, _ = FeedEntry.objects.update_or_create(
        feed=feed,
        link=parsed_entry.link,
        defaults={
            "title": parsed_entry.title,
            "published": make_aware(
                datetime.datetime(*parsed_entry.published_parsed[0:6])
            ),
            "summary": parsed_entry.summary,
        },
    )
    return entry
