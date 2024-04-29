import feedparser
from time import mktime
from requests import get
from telepotpro import Bot
from datetime import datetime
from pony.orm import db_session
from modules import settings
from modules.database import Video

bot = Bot(settings.get("BOT_TOKEN"))


def pt_to_seconds(duration: str) -> int:
    # https://developers.google.com/youtube/v3/docs/videos#contentDetails.duration
    duration = duration.replace("PT", "")
    seconds = 0
    if "H" in duration:
        hours, duration = duration.split("H")
        seconds += int(hours) * 3600
    if "M" in duration:
        minutes, duration = duration.split("M")
        seconds += int(minutes) * 60
    if "S" in duration:
        seconds += int(duration.split("S")[0])
    return seconds


def get_video_duration(video_id: str) -> int:
    res = get("https://youtube.googleapis.com/youtube/v3/videos",
              headers={"Accept": "application/json"},
              params={
                  "part": "contentDetails",
                  "id": video_id,
                  "key": settings.get("YOUTUBE_APIKEY")
              })

    duration = res.json()["items"][0]["contentDetails"]["duration"]
    return pt_to_seconds(duration)


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
            # Scarta shorts
            duration = get_video_duration(video.id)
            if duration > 90:
                send_news(video)
            video.processed = True
