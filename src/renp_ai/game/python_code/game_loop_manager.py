class GameLoopManager:
    def __init__(self, display_manager, context_manager):
        self.display_manager = display_manager
        self.context_manager = context_manager
        self.logger = Logger(os.path.join(base_dir, "log_custom.txt"))

    def start_initial_loop(self):
        if not self.display_manager.api_manager.api_key_manager.api_key:
            self.display_manager.run_first_time_setup()

        # set the default scene
        self.display_manager.change_scene(self.context_manager.scene.location)

        # choice` is a dictionary with the following structure:
        #  {"choice": "text1", "flags": ["location"]}
        choice = {
            "choice": DEFAULT_PROMPT,
            "flags": []
        }

        options = self.display_manager.handle_choice_and_get_response(choice)

        return self.start_normal_loop(options)

    def start_normal_loop(self, options):

        # Example of options structure: [
        #     {"choice": "text1", "flags": ["location"]},
        #     {"choice": "text2", "flags": []},
        #     {"choice": "text3", "flags": []},
        #     {"choice": "text4", "flags": []}
        # ]

        while options:
            choice = self.display_manager.display_menu(options)

            # 'choice' should always be a dictionary containing 'choice' and 'flags'
            flags = choice.get('flags', [])

            if 'location' in flags:
                # Inform ContextManager about the location change
                new_location = self.context_manager.handle_location_change(choice)
                # After the context manager updates the location, inform the display manager
                self.display_manager.change_scene(new_location)

            #  options is a list of dictionaries with the following structure:
            #  [{"choice": "text1", "flags": ["location"]}]
            options = self.display_manager.handle_choice_and_get_response(choice)

        return "end"
