# This file contains the Location class, which represents a location in the game.
# game/python_code/constructs/location.py
class Location:
    def __init__(self, name, prompt, description=None, filepath=None):
        self.name = name
        self.prompt = prompt
        self.description = description
        if filepath:
            self.filepath = filepath
        else:
            self.filepath = self.name.replace(" ", "_") + ".png"

    def get_location_details(self):
        return {
            'Name': self.name,
            "Description": self.description,
        }

    def set_description(self, description):
        self.description = description