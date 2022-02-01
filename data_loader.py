import json


def load_bot_data():
    with open("data/data.json", "r", encoding="utf-8") as bot_data:
        data = json.load(bot_data)
    meeting_data = data[0]
    profile_data = data[1]

    with open("txt/messages.txt", "r", encoding="utf-8") as msg_data:
        message_data = msg_data.read().split("***")

    return meeting_data, profile_data, message_data


def update_bot_data(meeting_data: list, profile_data: list):
    with open("data/data.json", "w", encoding="utf-8") as bot_data:
        json.dump([meeting_data, profile_data], bot_data, indent=4, ensure_ascii=False)
