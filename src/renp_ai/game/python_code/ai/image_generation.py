# game/python_code/ai/image_generation.py
class ImageGenerator:

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        log_message(os.path.join(config.gamedir, "image_generation_log.txt"))

    def create_displayable(self, image_filepath):
        if not os.path.exists(image_filepath):
            log_message(f"Image file does not exist at path: {image_filepath}")
            raise FileNotFoundError(f"The image file at {image_filepath} does not exist.")
        return im.Image(image_filepath)

    def generate_image(self, prompt):
        # Construct URL to request image from the API
        encoded_prompt = prompt.replace(' ', '%20')
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # This will raise an exception for HTTP error codes

            # Create a filename for the image based on the prompt
            image_filename = f"{prompt.replace(' ', '_')}.png"
            image_filepath = os.path.join(cache_dir, image_filename).replace("\\", "/")

            # Save the image file to the designated path
            with open(image_filepath, 'wb') as file:
                file.write(response.content)

            # Log successful image retrieval and saving
            log_message(f"Image successfully retrieved and saved at {image_filepath}")

            return image_filepath  # Return the filepath for further use

        except requests.exceptions.RequestException as e:
            log_message(f"Error generating image: {str(e)}")
            return None