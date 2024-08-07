init python:

    import requests
    import json
    import os

    log_file_path = os.path.join(config.basedir, "log_custom.txt")

    def log_message(message):
        with open(log_file_path, "a") as log_file:
            log_file.write(message + "\n")

    # Function to get LLM response
    def get_llm_response(user_message, chat_history, model=DEFAULT_MODEL.value, max_tokens=DEFAULT_MAX_TOKENS):
        if not api_key:
            return None  # Return None if the API key is not set

        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Prepare the system message to instruct the LLM
        system_message = {
            "role": "system",
            "content": (
                "You are a narrator in a text-based adventure game. The user will read your narration first, then select one of the choices you provide in order to continue the story. "
                "Provide your response in the following JSON format without any line breaks: "
                "{\"narration\": \"string\", \"choices\": [\"string\",\"string\",\"string\",\"string\"]} "
                "If your response is not valid JSON conforming to this schema the response will be rejected! "
                "Ensure there are between 2 and 4 interesting and contextually relevant choices to progress the story."
            )
        }

        # Prepare the messages with chat history
        messages = [system_message] + chat_history.get_history() + [
            {
                "role": "user",
                "content": user_message
            }
        ]

        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages
        }

        # Log the payload for debugging
        log_message("Payload: " + json.dumps(payload, indent=2))

        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raise an error for bad responses
            result = response.json()

            assistant_message = result['choices'][0]['message']['content'].strip()
            log_message("Assistant response: " + assistant_message)

            return assistant_message  # Return the plain assistant message
        except requests.exceptions.RequestException as e:
            log_message("API request failed: " + str(e))
            return None  # Return None if there is an error with the API request

    # Function to validate the response
    def validate_response(response):
        try:
            data = json.loads(response)
            choices = data.get('choices', None)

            # Log the type for debugging
            log_message(f"Type of choices: {type(choices).__name__}")

            # Check if 'choices' behaves like a list
            if not hasattr(choices, '__iter__') or not hasattr(choices, 'append'):
                log_message("Error - Choices is not list-like.")
                return False, {}

            # Check the number of items in 'choices'
            if not (2 <= len(choices) <= 4):
                log_message(f"Error - Choices should contain between 2 and 4 items, found {len(choices)}")
                return False, {}

            # Check that each choice is a string
            for choice in choices:
                if not isinstance(choice, str):
                    log_message("Error - Each choice should be a string.")
                    return False, {}

            return True, data

        except json.JSONDecodeError as e:
            log_message(f"Error - Invalid JSON format: {str(e)}")
            return False, {}



    # Function to parse multi-line responses and extract options
    def parse_response(response, max_line_length=DEFAULT_MAX_LINE_LENGTH):
        # Split the response into lines
        lines = response.split('\n')
        formatted_response = []
        options = []

        for line in lines:
            line = line.strip()
            if line.startswith("Option: "):
                options.append(line[len("Option: "):].strip())
            else:
                # Use a buffer to collect segments of the line
                buffer = ""
                while len(line) > 0:
                    # Find the position to break the line
                    break_pos = -1
                    if len(line) <= max_line_length:
                        break_pos = len(line)
                    else:
                        # Prioritize breaking at periods, semicolons, and colons
                        for punct in ['.', ';', ':']:
                            pos = line.find(punct, 0, max_line_length)
                            if pos != -1:
                                break_pos = pos + 1
                                break
                        if break_pos == -1:
                            space_index = line.rfind(' ', 0, max_line_length)
                            if space_index == -1:
                                break_pos = max_line_length
                            else:
                                break_pos = space_index

                    # Add the segment to the buffer
                    buffer += line[:break_pos].strip()
                    line = line[break_pos:].strip()

                    # Add the buffer to the formatted response and reset buffer
                    formatted_response.append(buffer)
                    buffer = ""

        return formatted_response, options
