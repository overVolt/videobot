from telepotpro import Bot
from modules import settings

bot = Bot(settings.get("BOT_TOKEN"))


def send(text: str):
    return bot.sendMessage(settings.get("CHAT_ID"), text, parse_mode="HTML")
