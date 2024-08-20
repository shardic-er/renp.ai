class ResponseValidator:
    def __init__(self):
        pass

    def validate_response(self, response):
        try:
            data = json.loads(response)
            choices = data.get('choices', None)

            if not hasattr(choices, '__iter__') or not hasattr(choices, 'append'):
                log_message("Error - Choices is not list-like.")
                return False, {}

            if not (2 <= len(choices) <= 4):
                log_message(f"Error - Choices should contain between 2 and 4 items, found {len(choices)}")
                return False, {}

            for choice in choices:
                if not isinstance(choice, str):
                    log_message("Error - Each choice should be a string.")
                    return False, {}

            return True, data

        except json.JSONDecodeError as e:
            log_message(f"Error - Invalid JSON format: {str(e)}")
            return False, {}

    def validate_response_retry_until_valid(self, llm_client, assistant_message, user_message, max_retries=3):
        retries = 0
        while retries < max_retries:
            is_valid, validation_result = self.validate_response(assistant_message)
            if is_valid:
                return validation_result  # Return validated response
            else:
                log_message(f"Invalid response: {assistant_message}")
                retries += 1
                if retries < max_retries:
                    log_message(f"Retrying... ({retries}/{max_retries})")
                    assistant_message = llm_client.get_llm_response(user_message)
                else:
                    log_message("Max retries reached. No valid response received.")
                    return None

    def sanitize_choice_text_and_extract_flags(self, choice_text):
        # Regular expression to match anything within curly braces {}
        flag_pattern = r'\{([^}]+)\}'

        # Find all flags matching the pattern
        flags = re.findall(flag_pattern, choice_text)

        # Remove the flags from the choice text
        sanitized_text = re.sub(flag_pattern, '', choice_text).strip()

        return sanitized_text, flags

    def parse_response(self, response, max_line_length):
        is_valid, parsed_data = self.validate_response(response)
        if not is_valid:
            log_message("Validation failed.")
            return ["Invalid response received."], []

        narration = parsed_data["narration"]
        choices = parsed_data["choices"]

        # Sanitize the choices and extract flags
        sanitized_choices = []
        for choice in choices:
            sanitized_text, flags = self.sanitize_choice_text_and_extract_flags(choice)
            sanitized_choices.append({"choice": sanitized_text, "flags": flags})

        formatted_response = self.format_narration(narration, max_line_length)

        return formatted_response, sanitized_choices

    def format_narration(self, narration, max_line_length):
        formatted_response = []
        while len(narration) > max_line_length:
            break_pos = -1
            for punct in ['.', ';', ':']:
                pos = narration.find(punct, 0, max_line_length)
                if pos != -1:
                    break_pos = pos + 1
                    break
            if break_pos == -1:
                space_index = narration.rfind(' ', 0, max_line_length)
                if space_index == -1:
                    break_pos = max_line_length
                else:
                    break_pos = space_index
            formatted_response.append(narration[:break_pos].strip())
            narration = narration[break_pos:].strip()
        if narration:
            formatted_response.append(narration)
        return formatted_response
