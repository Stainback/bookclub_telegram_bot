from config import LANG
from data_loader import collection_meetings, collection_profiles, collection_localizations


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

    def __init__(self, editor_id: int, id_db: int):
        self.id_num = editor_id
        self.id_db = id_db
        self.cursor = 0

    def create_empty_meeting(self):
        collection_meetings.insert_one(self.template)

    def edit_property(self, text: str):
        if 0 < self.cursor <= len(list(self.template["data"].keys())):
            collection_meetings.update_one({"_id": self.id_db},
                                           {"$set": {list(self.template["data"].keys())[self.cursor - 1]: text}})

    def generate_meeting_text(self):
        meeting_data = collection_meetings.find_one({"_id": self.id_db})
        meeting_text = f"\n{meeting_data['topic']}. {meeting_data['meeting_date']}, {meeting_data['meeting_time']}." \
                       f"\n{meeting_data['location']}\n{meeting_data['comment']}\n"
        return meeting_text


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
            # Reserve "member_name" property update
            if self.cursor == 0:
                self.edit_property("member_name", text)
            # Reserve "birth_date" property update
            if self.cursor == 2:
                self.edit_property("birth_date", text)
            collection_profiles.update_one({"_id": self.id_num},
                                           {"$set": {list(self.form.keys())[self.cursor - 1]: text}})

    def generate_form_text(self):
        form_data = collection_profiles.find_one({"_id": self.id_num})["form"]
        form_text = ""
        i = 1
        for q_id in list(self.form.keys()):
            if form_data[q_id] != "":
                form_text += f"\n{i}. {self.form[q_id]}\n     {form_data[q_id]}\n"
        return form_text


class BotContainer:

    def __init__(self, content_flag):
        self.container = []

        if content_flag in ("m", "p"):
            self.content_type = content_flag
        else:
            raise ValueError("Only 'm' and 'p' flags are allowed.")

    def add_object(self, obj):
        if self.content_type == "m":
            if isinstance(obj, Meeting):
                self.container.append(obj)
        if self.content_type == "p":
            if isinstance(obj, Profile):
                self.container.append(obj)
        else:
            raise ValueError("Only Profiles or Meetings can be added to the container.")

    def find_object(self, id_num: int):
        for obj in self.container:
            if obj.id_num == id_num:
                return obj
        raise ValueError(f"Profile object with id {id_num} does not found.")

    def remove_object(self, id_num):
        for obj in self.container:
            if obj.id_num == id_num:
                self.container.pop(obj)
                print(f"Object with id {id_num} has been removed from container.")
                return
