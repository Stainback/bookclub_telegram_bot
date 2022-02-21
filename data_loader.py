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
    except CursorNotFound:
        pass


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
        # If file has .txt extension
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as msg_data:
                message_data = {item.split("<id>")[0]: item.split("<id>")[1] for item in msg_data.read().split("<bl>")}
        # If file has .json extension
        if file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as bot_data:
                message_data: dict = json.load(bot_data)
        collection_localizations.insert_one({
                                                "_id": lang,
                                                "prompts": message_data
                                            })


