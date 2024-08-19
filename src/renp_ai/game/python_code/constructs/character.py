# game/python_code/constructs/character.py
class Character:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        # self.renpy_character = renpy_character

    def get_character_details(self):
        details = {
            "name": self.name,
            "description": self.description
        }
        return details
