import json

from pymongo import MongoClient
from pymongo.errors import CursorNotFound

from config import DB_URL, LANG

client = MongoClient(DB_URL)
db = client["bc_tbotDB"]

collection_profiles = db["profiles"]
collection_meetings = db["meetings"]
collection_localizations = db["localizations"]


def get_message_prompt(prompt_id: str, lang=LANG) -> str:
    try:
        localization = collection_localizations.find_one({"_id": lang})
        return localization["prompts"][f"{prompt_id}"]
    except CursorNotFound as err:
        print(err)


def create_message_prompt(prompt_id: str, prompt_text: str, lang=LANG):
    try:
        collection_localizations.update_one({"_id": lang}, {"$set": {prompt_id: prompt_text}})
    except CursorNotFound:
        post = {
                "_id": lang,
                "prompts": {prompt_id: prompt_text}
                }
        collection_localizations.insert_one(post)


def create_localization_from_file(file_path: str, lang=LANG):
    if collection_localizations.count_documents({"_id": lang}) == 0:
        if file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as bot_data:
                message_data: dict = json.load(bot_data)
            collection_localizations.insert_one({
                                                    "_id": lang,
                                                    "prompts": message_data
                                                })
        else:
            raise TypeError("Localization file must have .json extension")
    else:
        print("Localization already exists.")


def generate_meeting_messages(search_request: dict) -> dict:
    result = {}
    search_result = collection_meetings.find(search_request)
    if search_result is not None:
        for meeting in collection_meetings.find(search_request):
            meeting_data = meeting["data"]
            # Generate message text for a meeting
            meeting_text = f"\n{meeting_data['topic']}. {meeting_data['meeting_date']}, {meeting_data['meeting_time']}." \
                           f"\n{meeting_data['location']}\n{meeting_data['comment']}\n"
            result[meeting["_id"]] = meeting_text
    return result

