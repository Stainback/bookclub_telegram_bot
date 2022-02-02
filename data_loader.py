import json


def load_bot_data():
    with open("data/data_meetings.json", "r", encoding="utf-8") as bot_data:
        data = json.load(bot_data)
    meeting_data = data

    with open("data/data_profiles.json", "r", encoding="utf-8") as bot_data:
        data = json.load(bot_data)
    profile_data = data

    with open("data/messages.txt", "r", encoding="utf-8") as msg_data:
        message_data = msg_data.read().split("***")

    return meeting_data, profile_data, message_data


def update_mbot_data(meeting_data: list):
    with open("data/data_meetings.json", "w", encoding="utf-8") as bot_data:
        json.dump(meeting_data, bot_data, indent=4, ensure_ascii=False)


def update_pbot_data(profile_data: list):
    with open("data/data_profiles.json", "w", encoding="utf-8") as bot_data:
        json.dump(profile_data, bot_data, indent=4, ensure_ascii=False)
