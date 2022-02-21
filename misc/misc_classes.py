from config import LANG
from data.main_db import collection_meetings, collection_profiles, collection_localizations


class Meeting:

    template = {
                    "data": {
                                "meeting_date": "",
                                "meeting_time": "",
                                "topic": "",
                                "location": "",
                                "comment": ""
                            }
                }

    def __init__(self, id_num: int, editor_id: int):
        self.id_num = id_num
        self.cursor = 0
        self.edited_by = editor_id

    def create_empty_meeting(self):
        collection_meetings.insert_one({"_id": self.id_num, **self.template})

    def edit_property(self, text: str):
        if 0 < self.cursor <= 5:
            collection_meetings.update_one({"_id": self.id_num},
                                           {"$set": {list(self.template["data"].keys())[self.cursor - 1]: text}})
        else:
            pass

    def get_data(self):
        return collection_meetings.find_one({"_id": self.id_num})["data"]


class Profile:

    form = {m_id: "" for m_id in list(collection_localizations.find_one({"_id": LANG})["prompts"].keys())
            if m_id.startswith("msg_userform")}

    template = {
                    "member_name": "",
                    "username": "",
                    "birth_date": "",
                    "form": {"form_id": 0, **form}
                }

    def __init__(self, user_id: int):
        self.id_num = user_id
        self.cursor = 0

    def create_empty_profile(self):
        collection_profiles.insert_one({"_id": self.id_num, **self.template})

    def edit_property(self, prop: str, text: str):
        collection_profiles.update_one({"_id": self.id_num}, {"$set": {prop: text}})

    def edit_form_field(self, text: str):
        if 0 < self.cursor <= len(list(self.form.keys())):
            collection_profiles.update_one({"_id": self.id_num},
                                           {"$set": {list(self.form.keys())[self.cursor - 1]: text}})
        else:
            pass

