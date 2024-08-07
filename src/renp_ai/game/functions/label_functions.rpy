# label_functions.rpy

default options = []

label initialize_configs:
    $ prompt = "Hi."
    $ selected_model = DEFAULT_MODEL.value
    $ max_tokens = DEFAULT_MAX_TOKENS
    return

label save_api_key:
    $ api_key = renpy.input("Please enter your API key:", length=200)
    return

label first_time_setup:
    "Welcome to the game!"
    "This game requires an API key from OpenAI to function properly."
    while True:
        call save_api_key
        # Check if the API key is valid by making a ping request
        $ test_response = get_llm_response("Hello!", chat_history)
        if test_response is not None:
            "API key saved successfully."
            return
        else:
            "API key is invalid. Please try again."

label get_parsed_llm_response:
    $ prompt = renpy.input("Enter your prompt:")

    # Log chat history for debugging
    $ log_message("Chat History: " + json.dumps(chat_history.get_history(), indent=2))

    $ retries = 0
    $ max_retries = 3
    $ valid_response_received = False

    while retries < max_retries and not valid_response_received:
        $ assistant_message = get_llm_response(prompt, chat_history, model=selected_model, max_tokens=max_tokens)

        # Check if the API key is missing or invalid
        if assistant_message is None:
            "Chat completion is not reachable at this time."
            "You may have an issue with your network connection, or your API key might be missing or invalid."

            menu:
                "Choose an option to continue."
                "Retry connection":
                    jump get_parsed_llm_response
                "Input api key":
                    jump first_time_setup

        # Validate the LLM response
        $ is_valid, response_data = validate_response(assistant_message)

        if is_valid:
            $valid_response_received = True
        else:
            "Received invalid response from the assistant. Retrying..."
            $log_message("Invalid response: " + assistant_message)
            $retries += 1


    if not valid_response_received:
        "Max retries reached. No valid response received."
        return




    # Add user and assistant messages to chat history
    $ chat_history.add_message("user", prompt)
    $ chat_history.add_message("assistant", assistant_message)

    # Extract narration and options
    if valid_response_received:
        $ narration = response_data.get("narration", "")
        $ options = response_data.get("choices", [])

    # Show the narration
    "[narration]"

    # Handle options for the next step
    if options:
        call display_dynamic_menu
    else:
        $ prompt = renpy.input("Enter your next prompt:")
        call get_parsed_llm_response

    return

label display_dynamic_menu:
    python:
        menu_items = [(opt, opt) for opt in options]

    $ choice = renpy.display_menu(menu_items)

    $ prompt = choice
    call get_parsed_llm_response

    return

label end:
    "This is the end of the loop."
