class LLMClient:
    def __init__(self, context_manager, model, max_tokens, api_key_manager, logger):
        self.context_manager = context_manager
        self.selected_model = model
        self.max_tokens = max_tokens
        self.api_key_manager = api_key_manager
        self.logger = logger

    def get_llm_response(self, user_message):
        if not self.api_key_manager.api_key:
            self.logger.log_message("API key is missing.")
            return None

        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key_manager.api_key}",
            "Content-Type": "application/json"
        }

        # Constructing the message context with the system prompt and user message
        messages = self.context_manager.get_context() + [
            {"role": "user", "content": user_message}
        ]

        payload = {
            "model": self.selected_model,
            "max_tokens": self.max_tokens,
            "messages": messages
        }

        self.logger.log_message("Payload: " + json.dumps(payload, indent=2))

        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()

            assistant_message = result['choices'][0]['message']['content'].strip()

            return assistant_message
        except requests.exceptions.RequestException as e:
            error_detail = e.response.text
            self.logger.log_message(f"API request failed: {str(e)} - {error_detail}")
            return None

    def imagine_location_name_and_description(self, choice):
        if not self.api_key_manager.api_key:
            self.logger.log_message("API key is missing.")
            return None

        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key_manager.api_key}",
            "Content-Type": "application/json"
        }

        # Correctly constructing the message context with the system prompt and user message
        # Given that it is a list of dicts
        message_content_info = "History: " + "".join(
            str(item) for item in self.context_manager.get_filtered_context_by_role("assistant"))

        message_history = {
            "role": "system",
            "content": message_content_info
        }
        scene_context = {
            "role": "system",
            "content": "Current scene context: " + json.dumps(self.context_manager.get_scene_context())
        }
        user_choice = {
            "role": "user",
            "content": choice.get('choice')
        }
        instruction_context = {
            "role": "system",
            "content": ("You are part of a multi-agent content generation system. "
                        "Using the context provided above, respond with the name of a location"
                        "that the user chose along with a descriptive prompt to be used for image generation."
                        "for example: if the user responded: go deeper into the forest, you could respond with: "
                        "{\"name\":\"deeper_forest\", \"description\":\"A dense and mysterious forest, with tall, ancient trees whose thick branches form a canopy overhead. The ground is covered in a thick layer of moss and scattered with fallen leaves and branches. Sunlight filters through in beams, creating a dappled effect on the forest floor. The atmosphere is quiet, with only the sounds of distant wildlife and the rustle of leaves.\"}"
                        )

        }
        messages = [
            message_history,
            scene_context,
            user_choice,
            instruction_context
        ]

        payload = {
            "model": self.selected_model,
            "max_tokens": self.max_tokens,
            "messages": messages
        }

        self.logger.log_message("Payload: " + json.dumps(payload, indent=2))

        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()

            assistant_message = result['choices'][0]['message']['content'].strip()

            return assistant_message
        except requests.exceptions.RequestException as e:
            error_detail = e.response.text
            self.logger.log_message(f"API request failed: {str(e)} - {error_detail}")
            return None