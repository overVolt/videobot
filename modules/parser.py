# Incoming XML atom feed
def parse_feed(feed):
    """Parse the incoming XML atom feed."""
    # Parse the feed
    feed = feedparser.parse(feed)
    # Get the feed title
    feed_title = feed.feed.title
    # Get the feed entries
    feed_entries = feed.entries
    # Return the feed title and entries
    return feed_title, feed_entries
