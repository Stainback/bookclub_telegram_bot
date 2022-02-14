import json

from misc import Meeting, Profile


def load_message_data():
    with open("data/messages.txt", "r", encoding="utf-8") as msg_data:
        data = msg_data.read().split("***")
    message_data = {item.split("/")[0]: item.split("/")[1] for item in data}
    return message_data


def load_bot_data():
    with open("data/data_meetings.json", "r", encoding="utf-8") as bot_data:
        data = json.load(bot_data)
    meeting_data = [Meeting(item) for item in data]

    with open("data/data_profiles.json", "r", encoding="utf-8") as bot_data:
        data = json.load(bot_data)
    profile_data = [Profile(item[0], item[1]) for item in data]

    return meeting_data, profile_data


def update_bot_data(objects: list, file_path: str):
    """
        Use for updating meetings and profiles data.
    """

    with open(file_path, "w", encoding="utf-8") as bot_data:
        json.dump(objects, bot_data, indent=4, ensure_ascii=False)
