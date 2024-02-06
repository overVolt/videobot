import feedparser
from time import mktime
from telepotpro import Bot
from datetime import datetime
from pony.orm import db_session
from modules import settings
from modules.database import Video

bot = Bot(settings.get("BOT_TOKEN"))


@db_session
def send_news(video: Video):
    bot.sendMessage(settings.get("CHAT_ID"), parse_mode="HTML",
                    text=f"Nuovo video su {video.author}!\n\n"
                         f"<b>{video.title}</b>\n\n"
                         f"Guardalo ora! youtu.be/{video.id}")


@db_session
def parse_feed(feed: str):
    parsed_feed = feedparser.parse(feed)
    for entry in parsed_feed["entries"]:
        if not (video := Video.get(id=entry["yt_videoid"])):
            video = Video(
                id=entry["yt_videoid"],
                title=entry["title"],
                author=entry["author"],
                publish_time=datetime.fromtimestamp(mktime(entry["published_parsed"]))
            )

        if not video.processed:
            send_news(video)
            video.processed = True
