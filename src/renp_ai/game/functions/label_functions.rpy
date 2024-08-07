# label_functions.rpy

default options = []

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

label initialize_configs:
    $ prompt = "Hi."
    $ selected_model = DEFAULT_MODEL.value
    $ max_tokens = DEFAULT_MAX_TOKENS
    return

label get_parsed_llm_response:
    $ prompt = renpy.input("Enter your prompt:")

    # Log chat history for debugging
    $ log_message("Chat History: " + json.dumps(chat_history.get_history(), indent=2))

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

    # Add user and assistant messages to chat history
    $ chat_history.add_message("user", prompt)
    $ chat_history.add_message("assistant", assistant_message)

    # Validate and parse the LLM response
    $ parsed_data = validate_response_retry_until_valid(assistant_message, prompt, chat_history, selected_model, max_tokens)
    if not parsed_data:
        "The assistant provided an invalid response. Please try again."
        jump get_parsed_llm_response

    $ response_lines, options = parse_response(json.dumps(parsed_data))

    # Show the LLM response
    $ i = 0
    while i < len(response_lines):
        $ line = response_lines[i]
        "[line]"
        $ i += 1

    # Handle options for the next step
    call display_dynamic_menu

    return

label display_dynamic_menu:
    python:
        menu_items = [(opt, opt) for opt in options]

    $ choice = renpy.display_menu(menu_items)

    # Treat the selected option as the next prompt
    $ prompt = choice
    $ chat_history.add_message("user", prompt)
    $ assistant_message = get_llm_response(prompt, chat_history, model=selected_model, max_tokens=max_tokens)

    # Add user and assistant messages to chat history
    $ chat_history.add_message("assistant", assistant_message)

    # Validate and parse the LLM response
    $ parsed_data = validate_response_retry_until_valid(assistant_message, prompt, chat_history, selected_model, max_tokens)
    if not parsed_data:
        "The assistant provided an invalid response. Please try again."
        jump get_parsed_llm_response

    $ response_lines, options = parse_response(json.dumps(parsed_data))

    # Show the LLM response
    $ i = 0
    while i < len(response_lines):
        $ line = response_lines[i]
        "[line]"
        $ i += 1

    # Handle options for the next step
    call display_dynamic_menu

    return
