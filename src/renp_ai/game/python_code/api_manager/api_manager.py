class APIManager:
    def __init__(self, context_manager, model, max_tokens, api_key_manager):
        self.api_key_manager = api_key_manager
        self.llm_client = LLMClient(context_manager, model, max_tokens, self.api_key_manager)
        self.response_validator = ResponseValidator()
        self.context_manager = context_manager

    def get_llm_response(self, user_message):
        return self.llm_client.get_llm_response(user_message)

    def imagine_location_name_and_description(self, choice):
        return self.llm_client.imagine_location_name_and_description(choice)

    def validate_response_retry_until_valid(self, assistant_message, user_message):
        return self.response_validator.validate_response_retry_until_valid(self.llm_client, assistant_message, user_message)

    def parse_response(self, response, max_line_length):
        return self.response_validator.parse_response(response, max_line_length)

    def save_api_key(self, key):
        self.api_key_manager.save_api_key(key)

    def validate_api_key(self):
        return self.api_key_manager.validate_api_key(self.llm_client)

