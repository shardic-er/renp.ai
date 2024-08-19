# script.rpy

define narrator = Character(None, kind=nvl, color="#ff0000")
image black_bg = Solid("#000000")

init python:
    import sys
    import os
    import glob
    import json
    import requests
    import re

    # Set the base directory to the actual location of the script file
    base_dir = "C:/Users/Shardic/Desktop/YorkSolutions/renpy_ai/src/renp_ai/game"
    python_modules_dir = os.path.join(base_dir, "python_code")
    audio_dir = os.path.join(base_dir, "audio")

    # Add the correct directory to sys.path
    sys.path.append(python_modules_dir)

    # Define the log file path early
    log_file_path = os.path.join(base_dir, "log_custom.txt")

    # Execute all .py files within the python_code directory
    for filepath in glob.glob(os.path.join(python_modules_dir, '**', '*.py'), recursive=True):
        exec(open(filepath).read())

    # Initialize the sound dictionary
    sound_dict = {}

    def initialize_sounds(directory, sound_dict):
    # Recursively initialize sounds from the given directory."
        for filepath in glob.glob(os.path.join(directory, '**', '*.mp3'), recursive=True):
            sound_name = os.path.basename(filepath)
            normalized_path = filepath.replace("\\", "/")
            sound_dict[sound_name] = normalized_path


    # Populate the sound dictionary with all sounds in the audio directory
    initialize_sounds(audio_dir, sound_dict)

    # Initialize the api key manager
    api_key_manager = APIKeyManager()

    # Initialize the ContextManager with the main prompt
    context_manager = ContextManager(
        system_prompt=SYSTEM_PROMPT,
        seed_prompt=DEFAULT_PROMPT,
        api_key_manager=api_key_manager
    )


    # Initialize components
    api_manager = APIManager(
        context_manager=context_manager,
        log_file_path=log_file_path,
        model=DEFAULT_MODEL,
        max_tokens=DEFAULT_MAX_TOKENS,
        api_key_manager=api_key_manager

    )
    display_manager = DisplayManager(narrator, sound_dict, api_manager, base_dir)
    game_loop_manager = GameLoopManager(display_manager, context_manager)

label start:
    python:
        context_manager.set_scene(default_scene)
        next_label = game_loop_manager.start_initial_loop()

    if next_label == "end":
        jump end

label end:
    "Quiting..."
    return