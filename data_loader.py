import json

from misc import Meeting, Profile


def load_bot_data():
    with open("data/data_meetings.json", "r", encoding="utf-8") as bot_data:
        data = json.load(bot_data)
    meeting_data = [Meeting(item) for item in data]

    with open("data/data_profiles.json", "r", encoding="utf-8") as bot_data:
        data = json.load(bot_data)
    profile_data = [Profile(item) for item in data]

    with open("data/messages.txt", "r", encoding="utf-8") as msg_data:
        data = msg_data.read().split("***")
    message_data = {item.split("/")[0]: item.split("/")[1] for item in data}

    print(meeting_data)
    print(profile_data)
    print(message_data)
    return meeting_data, profile_data, message_data


def update_mbot_data(meeting_objects: list):
    meeting_data = [meeting.data for meeting in meeting_objects]

    with open("data/data_meetings.json", "w", encoding="utf-8") as bot_data:
        json.dump(meeting_data, bot_data, indent=4, ensure_ascii=False)


def update_pbot_data(profile_objects: list):
    profile_data = [profile.data for profile in profile_objects]

    with open("data/data_profiles.json", "w", encoding="utf-8") as bot_data:
        json.dump(profile_data, bot_data, indent=4, ensure_ascii=False)
