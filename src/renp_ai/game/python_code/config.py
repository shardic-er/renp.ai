# config.py

# Simple Enum implementation using a class, avoiding the use of Python's enum module
class ModelSelection:
    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4o = "gpt-4o"


class RecognizedFlags:
    LOCATION = "[location]"


# Default configurations
DEFAULT_MAX_CHAT_HISTORY_LENGTH = 2
DEFAULT_MODEL = ModelSelection.GPT_4o
DEFAULT_MAX_TOKENS = 4000
DEFAULT_IMAGE_DESCRIPTION_MAX_LENGTH = 250
DEFAULT_MAX_LINE_LENGTH = 250
DEFAULT_USER_NAME = "user"
DEFAULT_PROMPT = "write me a long story about walking through a dark wood"
SYSTEM_PROMPT = (
    "You are a narrator in a text-based adventure game. The user will read your narration first, then the user will respond with one of the choices you provide in order to continue the story. "
    "Provide your response in the following JSON format without any line breaks: "
    "{\"narration\": \"string\", \"choices\": [\"string\",\"string\",\"string\",\"string\"]} "
    "Ensure there are between 2 and 4 interesting and contextually relevant choices to progress the story."
    "Within the text of your choices, use the following system flags to indicate special actions: "
    "[location] - indicates a location change, a new background image will be displayed"
    "for example: {\"narration\": \"You find yourself at a crossroads.\", \"choices\": [\"Go left {location}\",\"Go right {location}\"]}"
)
