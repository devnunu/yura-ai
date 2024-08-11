
class Settings:
    def __init__(self):
        self.default_tone = "친근하고 전문적인"
        self.text_generation_criteria = ["가독성", "명확성", "간결성"]
        self.custom_criteria = []

    def add_criteria(self, criteria):
        self.custom_criteria.append(criteria)

    def remove_criteria(self, criteria):
        if criteria in self.custom_criteria:
            self.custom_criteria.remove(criteria)

settings = Settings()
