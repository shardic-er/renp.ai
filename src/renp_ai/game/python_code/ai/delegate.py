class Delegate:
    def __init__(self, context_manager, api_manager):
        self.context_manager = context_manager
        self.api_manager = api_manager

    def validate_location_response(self, response):
        # Location response should look like this:
        # {
        #     "name": "deeper_forest",
        #     "description": "A dense and mysterious forest, with tall, ancient trees whose thick branches form a canopy overhead. The ground is covered in a thick layer of moss and scattered with fallen leaves and branches. Sunlight filters through in beams, creating a dappled effect on the forest floor. The atmosphere is quiet, with only the sounds of distant wildlife and the rustle of leaves."
        # }

        try:
            response = json.loads(response)
            if 'name' not in response:
                log_message("Missing 'name' key in response.")
                return False, {}
            if 'description' not in response:
                log_message("Missing 'description' key in response.")
                return False, {}
            return True, response

        except json.JSONDecodeError as e:
            log_message(f"Error - Invalid JSON format: {str(e)}")
            return False, {}

    def retry_until_valid(self, callback, validator, max_retries=3):
        retries = 0

        while retries < max_retries:
            response = callback()
            is_valid, validation_result = validator(response)
            if is_valid:
                return validation_result
            else:
                log_message(f"Invalid response: {response}")
                retries += 1
                if retries < max_retries:
                    log_message(f"Retrying... ({retries}/{max_retries})")
                else:
                    log_message("Max retries reached. No valid response received.")
                    return None

        return None

    def generate_location(self, choice):

        location_data_raw = self.api_manager.imagine_location_name_and_description(choice)

        validation_result, location_data = self.validate_location_response(location_data_raw)

        if validation_result:
            log_message(f"Location data: {location_data}")

            new_location = Location(
                name=location_data.get('name'),
                description=location_data.get('description')
            )

            return new_location
        else:
            raise ValueError("Invalid location data received from delegate.")
            return None
