# game/python_code/constructs/scene.py
class Scene:
    def __init__(self, description, location=None, characters=None):
        self.description = description
        self.location = location  # This should be a Location object
        self.characters = characters if characters else []  # List of Character objects

    def add_character(self, character):
        self.characters.append(character)

    def set_characters(self, characters):
        self.characters = characters

    def set_location(self, location):
        self.location = location

    def get_scene_details(self):
        details = {
            "description": self.description,
            "location": self.location.get_location_details(),
            "characters": [character.get_character_details() for character in self.characters]
        }
        return details
