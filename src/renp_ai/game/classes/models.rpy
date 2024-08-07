# classes/models.rpy

init python:
    from enum import Enum

    # Define an Enum for model selection
    class ModelSelection(Enum):
        GPT_3_5 = "gpt-3.5-turbo"
        GPT_4 = "gpt-4"
        GPT_4o = "gpt-4o"

    # Default configurations
    DEFAULT_MODEL = ModelSelection.GPT_4o
    DEFAULT_MAX_TOKENS = 512
    DEFAULT_MAX_LINE_LENGTH = 250
    DEFAULT_USER_NAME = "user"

#     write me a long story about walking through a dark wood