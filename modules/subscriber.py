import requests
from modules import settings

def _send(hub: str, topic: str, callback: str, action: str, verify_token: str=None) -> requests.Response:
    res = requests.post(hub, data={
        "hub.topic": topic,
        "hub.callback": callback,
        "hub.mode": action,
        "hub.verify": "sync",
        "hub.verify_token": verify_token,
    })
    return res

def _action(action: str, channel: str) -> requests.Response:
    return _send(
        hub=settings.get("HUB_URL"),
        topic=f"https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel}",
        callback=settings.get("CALLBACK_URL"),
        action=action,
        verify_token=settings.get("VERIFY_TOKEN")
    )

def subscribe(channel: str) -> requests.Response:
    return _action("subscribe", channel)


def unsubscribe(channel: str) -> requests.Response:
    return _action("unsubscribe", channel)


def subscribe_all() -> list[requests.Response]:
    return [_action("subscribe", channel) for channel in settings.get("channels")]


def unsubscribe_all() -> list[requests.Response]:
    return [_action("unsubscribe", channel) for channel in settings.get("channels")]
