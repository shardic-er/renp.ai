# script.rpy

# import functions
call expression "functions/python_functions.rpy"
call expression "functions/label_functions.rpy"
call expression "functions/api_functions.rpy"

# import characters
call expression "characters/characters.rpy"

# import classes
call expression "classes/chat_history.rpy"
call expression "classes/models.rpy"

default chat_history = ChatHistory()
default api_key = None

# Define the script
label start:

    # Call first time setup to ensure API key is present and valid
    if not api_key:
        call first_time_setup

    # Setup
    call initialize_configs

    # main game loop
    while True:

         # Get and display the LLM response
        call get_parsed_llm_response

        # Display a menu with choices
        menu:
            "Choose an option to continue."

            "Continue":
                "You chose to continue."

            "Exit":
                "You chose to exit."
                jump end
