# response_handling.py

class ResponseHandler:

    def __init__(self, context_manager, get_llm_response, validate_response_retry_until_valid, parse_response, renpy_say):
        self.context_manager = context_manager
        self.get_llm_response = get_llm_response
        self.validate_response_retry_until_valid = validate_response_retry_until_valid
        self.parse_response = parse_response
        self.renpy_say = renpy_say
        self.options = []

    def get_parsed_llm_response(self, prompt, selected_model, max_tokens):
        assistant_message = self.get_llm_response(prompt, self.context_manager, model=selected_model, max_tokens=max_tokens)

        if assistant_message is None:
            self.renpy_say("Chat completion is not reachable at this time.")
            self.renpy_say("You may have an issue with your network connection, or your API key might be missing or invalid.")
            return None

        # Validate and parse the LLM response
        parsed_data = self.validate_response_retry_until_valid(assistant_message, prompt, self.context_manager, selected_model, max_tokens)
        if not parsed_data:
            self.renpy_say("The assistant provided an invalid response. Please try again.")
            return None

        response_lines, self.options = self.parse_response(parsed_data)

        # Show the LLM response incrementally
        for line in response_lines:
            self.renpy_say(line)

        return self.options


