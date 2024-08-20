class LLMClient:
    def __init__(self, context_manager, model, max_tokens, api_key_manager):
        self.context_manager = context_manager
        self.selected_model = model
        self.max_tokens = max_tokens
        self.api_key_manager = api_key_manager

    def get_llm_response(self, user_message):
        if not self.api_key_manager.api_key:
            log_message("API key is missing.")
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

        log_message("Payload: " + json.dumps(payload, indent=2))

        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()

            assistant_message = result['choices'][0]['message']['content'].strip()

            return assistant_message
        except requests.exceptions.RequestException as e:
            error_detail = e.response.text
            log_message(f"API request failed: {str(e)} - {error_detail}")
            return None

    def imagine_location_name_and_description(self, choice):
        if not self.api_key_manager.api_key:
            log_message("API key is missing.")
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

        log_message("Payload: " + json.dumps(payload, indent=2))

        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()

            assistant_message = result['choices'][0]['message']['content'].strip()

            return assistant_message
        except requests.exceptions.RequestException as e:
            error_detail = e.response.text
            log_message(f"API request failed: {str(e)} - {error_detail}")
            return None

    def log_safe_payload(self, payload):
        # Make a deep copy of the payload to avoid modifying the original one
        safe_payload = json.loads(json.dumps(payload))

        # Traverse the messages to find any base64 encoded image data
        for message in safe_payload.get("messages", []):
            for content_item in message["content"]:
                if content_item.get("type") == "image_url" and "url" in content_item["image_url"]:
                    # Replace the base64 image data with a placeholder string
                    content_item["image_url"]["url"] = "[base 64 encoded image omitted]"

        # Log the modified payload
        log_message("Payload: " + json.dumps(safe_payload, indent=2))

    def visualize_image_description(self, image_filepath):
        if not self.api_key_manager.api_key:
            log_message("API key is missing.")
            return None

        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key_manager.api_key}"
        }

        # Encode the image as a base64 string
        try:
            with open(image_filepath, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            log_message(f"Image file not found at path: {image_filepath}")
            return None
        except Exception as e:
            log_message(f"Failed to load image: {str(e)}")
            return None

        # Construct the message payload with the image encoded in base64
        payload = {
            "model": self.selected_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this scene."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": DEFAULT_IMAGE_DESCRIPTION_MAX_LENGTH
        }

        # Log the payload safely
        self.log_safe_payload(payload)

        try:
            # Send the POST request to the API
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            result = response.json()

            assistant_message = result['choices'][0]['message']['content'].strip()

            return assistant_message
        except requests.exceptions.RequestException as e:
            error_detail = e.response.text
            log_message(f"API request failed: {str(e)} - {error_detail}")
            return None


