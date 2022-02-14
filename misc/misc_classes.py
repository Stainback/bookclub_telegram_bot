import random

with open("data/messages.txt", "r", encoding="utf-8") as msg_data:
    data = msg_data.read().split("***")


class Meeting:

    properties = ["meeting_date", "meeting_time", "topic", "location", "comment"]

    def __init__(self, data=None):
        self.data = data or {prop: "" for prop in self.properties}
        self.meeting_id = random.randint(1000, 9999)
        self.owner_id = 0
        self.scenario_count = 0

    def set_owner(self, owner_id=0):
        self.owner_id = owner_id

    def fill_property(self, property_text=""):
        self.data[self.properties[self.scenario_count]] = property_text
        self.scenario_count += 1

    def generate_meeting_message(self) -> str:
        meeting_message = (f'\n\t Discussion topic - {self.data["topic"]}, {self.data["meeting_date"]} {self.data["meeting_time"]}.'
                           f'\n\t {self.data["location"]}\n')
        if self.data["comment"] != "":
            meeting_message += f'\t  {self.data["comment"]}\n'
        return meeting_message


class Profile:

    properties = ["member_name", "user_id", "username", "birth_date", "form_id"]
    form_questions = {item.split("/")[0]: item.split("/")[1]for item in data
                      if item.split("/")[0].startswith("msg_userform")}

    def __init__(self, data=None, form=None):
        self.data = data or {prop: "" for prop in self.properties}
        self.form = form or {q: "" for q in self.form_questions}
        self.scenario_count = 0

    def fill_form_field(self, property_text=""):
        self.form[list(self.form_questions.keys())[self.scenario_count]] = property_text
        self.scenario_count += 1

    def get_current_answer(self) -> str:
        return self.form[list(self.form_questions.keys())[self.scenario_count]]

    def erase_answers(self):
        self.form = {q: "" for q in self.form_questions}

    def generate_form_message(self) -> str:
        form_message = ""
        question_number = 1
        for (question, answer) in self.form.items():
            form_message += f"{question_number}. {self.form_questions[question]}      {answer}\n"
            question_number += 1
        return form_message


