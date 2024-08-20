class ContextManager:
    def __init__(self, system_prompt, api_key_manager, seed_prompt=None, max_history_length=DEFAULT_MAX_CHAT_HISTORY_LENGTH):
        self.system_prompt = system_prompt  # Persistent system prompt
        self.seed_prompt = seed_prompt  # Optional seed prompt for initial context
        self.chat_history = []  # List to hold the history of chat messages
        self.scene = None  # Optional scene object
        self.max_history_length = max_history_length  # Maximum length of chat history
        self.delegate = Delegate(
            self,
            APIManager(
                self,
                model=DEFAULT_MODEL,
                max_tokens=DEFAULT_MAX_TOKENS,
                api_key_manager=api_key_manager,
            )
        )

    def truncate_history(self):
        # Truncate the chat history if it exceeds the maximum length
        if len(self.chat_history) > self.max_history_length:
            self.chat_history = self.chat_history[-self.max_history_length:]

    def add_message(self, role, content):
        # Adds a message to the chat history.
        # :param role: 'system', 'user', or 'assistant'
        # :param content: The content of the message
        self.chat_history.append({"role": role, "content": content})
        # self.truncate_history()

    def get_context(self):
        # Returns the full chat context including the main system prompt and scene, if available.
        history = [{"role": "system", "content": self.system_prompt}]

        if self.seed_prompt:
            history.append({"role": "system", "content": self.seed_prompt})

        if self.scene:
            scene_message = self.scene.get_scene_details()
            history.append({"role": "system", "content": f"Scene: {scene_message}"})

        return history + self.chat_history

    def set_scene(self, scene):
        # Sets the scene object.
        # :param scene: The scene object to be serialized and included in the context
        self.scene = scene

    def clear_scene(self):
        # Clears the current scene object.
        self.scene = None

    def clear_history(self):
        # Clears the chat history.
        self.chat_history = []

    def handle_location_change(self, converted_choice):

        # Match an appropreate known location, or create a new one.
        ## PLACEHOLDER IMPLEMENTATION ALWAY RETURNS NEW LOCATION

        new_location = self.delegate_generation(converted_choice)

        # Handles a location change by updating the scene object.
        self.scene.set_location(new_location)

        # Set the description of the new location
        new_location.description = self.describe_image(new_location)

        return new_location

    def get_filtered_context_by_role(self, role):
        # Filter the chat history by role.
        return [message for message in self.chat_history if message['role'] == role]

    def get_scene_context(self):
        if self.scene:
            return self.scene.get_scene_details()
        else:
            return ""

    def delegate_generation(self, converted_choice, generation_type="location"):
        if generation_type == "location":
            new_location = self.delegate.generate_location(converted_choice)
            return new_location

    def describe_image(self, location):
        filepath = os.path.join(cache_dir, location.filepath).replace("\\", "/")
        image_description = self.delegate.api_manager.visualize_image_description(filepath)
        log_message("Image description: " + image_description)
        return image_description
