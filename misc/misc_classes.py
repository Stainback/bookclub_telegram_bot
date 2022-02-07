
class Meeting:

    def __init__(self, data=None):
        self.data = data
        self.properties = ("location", "meeting_date", "meeting_time", "topic", "comment", "meeting_id")
        self.scenario_count = 0

    def __repr__(self):
        if self.data is None:
            return "Empty meeting"
        return "/".join(list(self.data.values()))

    def fill_property(self, property_text: str):
        if self.data is None:
            self.data = {}
        self.data[self.properties[self.scenario_count]] = property_text
        self.scenario_count += 1

    def generate_meeting_id(self):
        self.data["meeting_id"] = self.data["meeting_date"].replace("-", "") + self.data["meeting_time"].replace(":", "")


class Profile:

    def __init__(self, data=None):
        self.data = data
        self.properties = ("member_name", "user_id", "username", "birth_date")
