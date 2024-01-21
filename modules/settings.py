import json

with open("settings.json", "r") as file:
    settings = json.load(file)


def get(key: str):
    return settings.get(key, None)
