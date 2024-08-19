class DisplayManager:
    def __init__(self, narrator, sound_dict, api_manager, base_dir):
        self.narrator = narrator
        self.sound_dict = sound_dict
        self.api_manager = api_manager
        self.base_dir = base_dir
        self.cache_dir = os.path.join(base_dir, "cache").replace("\\", "/")
        self.image_generator = ImageGenerator(self.cache_dir)
        self.logger = Logger(os.path.join(base_dir, "log_custom.txt"))

    def display_message(self, message):
        renpy.sound.play(self.sound_dict.get('button_click.mp3'))
        self.narrator(message)

    def display_menu(self, options):
        menu_items = [(opt['choice'], opt) for opt in options]
        choice_text_as_unparsed_string = renpy.display_menu(menu_items)
        renpy.sound.play(self.sound_dict.get('selection.mp3'))
        self.logger.log_message(f"User choice: {json.dumps(choice_text_as_unparsed_string)}")
        return choice_text_as_unparsed_string

    def format_and_display_response(self, response_lines):
        for line in response_lines:
            self.display_message(line)

    def validate_choice_data(self, choice):
        if not choice:
            self.api_manager.logger.log_message("Choice data is missing.")
            raise ValueError("Choice data is missing.")

        # Check if 'choice' behaves like a dictionary
        if not all(hasattr(choice, method) for method in ['get', 'items', '__contains__']):
            self.api_manager.logger.log_message("Choice data is not dictionary-like.")
            raise ValueError(f"Choice data is not dictionary-like, it is a: {type(choice)}")

        if 'choice' not in choice:
            self.api_manager.logger.log_message("Missing 'choice' key in choice data.")
            raise ValueError("Missing 'choice' key in choice data.")

        if 'flags' not in choice:
            self.api_manager.logger.log_message("Missing 'flags' key in choice data.")
            raise ValueError("Missing 'flags' key in choice data.")

        # If all checks pass, return True to indicate valid data
        return True

    def handle_choice_and_get_response(self, choice):

        # choice` is a dictionary with the following structure:
        #  {"choice": "text1", "flags": ["location"]}

        self.logger.log_message(f"Handling choice: {choice}")

        # Verify that it is infact a dictionary
        self.validate_choice_data(choice)

        # Convert the choice to a string
        user_message = self.parse_choice(choice)

        # Get the assistant response
        assistant_message = self.api_manager.get_llm_response(user_message)

        if assistant_message:
            # Process the assistant response
            return self.process_assistant_response(assistant_message, user_message)

        self.api_manager.logger.log_message("Failsafe triggered, returning None.")
        return None

    def parse_choice(self, choice):

        # choice` is a dictionary with the following structure:
        #  {"choice": "text1", "flags": ["location"]}

        choice_text = choice.get('choice', '')
        flags = choice.get('flags', [])

        # Add  any flags to the choice text
        for flag in flags:
            choice_text += f" {{{flag}}}"

        return choice_text

    def parse_choice_text_to_choice(self, choice_text_as_unparsed_string):

        # Convert the unparsed string to a dictionary
        choice_text_as_dict = json.loads(choice_text_as_unparsed_string)

        # Validate the choice data
        self.validate_choice_data(choice_text_as_dict)

        return choice_text_as_dict

    def process_assistant_response(self, assistant_message, user_message):
        # Validate the response
        parsed_data = self.api_manager.validate_response_retry_until_valid(
            assistant_message=assistant_message,
            user_message=user_message,
        )

        if parsed_data:
            self.update_context(user_message, assistant_message)
            return self.display_assistant_response(parsed_data)

        return None

    def display_assistant_response(self, parsed_data):
        # Parse the response and display it
        response_lines, options = self.api_manager.parse_response(
            response=json.dumps(parsed_data),
            max_line_length=DEFAULT_MAX_LINE_LENGTH
        )
        self.format_and_display_response(response_lines)

        # Check for flags and handle them
        self.handle_flags(options)

        return options

    def handle_flags(self, options):
        for option in options:
            flags = option.get('flags', [])
            if 'location' in flags:
                new_location = self.api_manager.llm_client.context_manager.scene.location
                if new_location:
                    self.change_scene(new_location)
                    self.api_manager.llm_client.context_manager.scene.set_location(new_location)

    def update_context(self, user_message, assistant_message):
        # Add the user choice to the context only after successful validation
        self.api_manager.llm_client.context_manager.add_message("user", user_message)
        # Add the assistant response to the context
        self.api_manager.llm_client.context_manager.add_message('assistant', assistant_message)

    def run_first_time_setup(self):
        self.display_message("Welcome to the game!")
        self.display_message("This game requires an API key from OpenAI to function properly.")

        while True:
            key = renpy.input("Please enter your API key:", length=200)
            self.api_manager.save_api_key(key)
            if self.api_manager.validate_api_key():
                self.display_message("API key saved successfully.")
                break
            else:
                self.display_message("API key is invalid. Please try again.")

        # Clear the chat history after setup to remove any test prompts
        self.api_manager.context_manager.clear_history()

    def change_scene(self, location):
        try:
            image_filename = f"{location.name.replace(' ', '_')}.png"
            image_filepath = os.path.join(self.cache_dir, image_filename).replace("\\", "/")

            # Check if the image exists, if not, generate it
            if not os.path.exists(image_filepath):
                self.api_manager.logger.log_message(f"No image found at {image_filepath}, generating new image.")
                image_filepath = self.image_generator.generate_image(location.name)
                if not image_filepath:
                    raise Exception("Failed to generate image.")

            # Load the image as an image displayable
            displayable = im.Image(image_filepath)

            # Get the screen size
            screen_width, screen_height = renpy.config.screen_width, renpy.config.screen_height

            # Assuming the original image is square, 512x512, and maintaining aspect ratio
            image_width = 512  # Original image width
            image_height = 512  # Original image height

            # Calculate the scaling factor
            width_scale = screen_width / image_width
            height_scale = screen_height / image_height

            # Use the smaller scale to maintain aspect ratio
            scale = min(width_scale, height_scale)

            # Calculate the new image size
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)

            # Apply the scaling to the image
            displayable = im.Scale(displayable, new_width, new_height)

            # Center the scaled image with Transform and align, with black borders filling the rest of the screen
            displayable = Transform(displayable, align=(0, 0.5))

            # Clear the current scene and show the transformed image
            renpy.scene("black")  # Clear the current scene
            renpy.show('bg', what=displayable)

        except Exception as e:
            self.api_manager.logger.log_message(f"Failed to load image for location '{location.name}': {str(e)}")
            self.display_message(f"Failed to load the scene image: {str(e)}")




