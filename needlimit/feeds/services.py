import datetime

import feedparser
from feeds.models import Feed, FeedEntry


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
            "last_updated": datetime.datetime(*parsed_feed.feed.updated_parsed[0:6]),
            "last_crawled": datetime.datetime.now(),
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
            "published": datetime.datetime(*parsed_entry.published_parsed[0:6]),
            "summary": parsed_entry.summary,
        },
    )
    return entry
