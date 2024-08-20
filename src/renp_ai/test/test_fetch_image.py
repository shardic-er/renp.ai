# Let's prepare the test script for the new Scene and Character functionality within the ContextManager

import os
import json
from src.renp_ai.game.python_code.constructs.location import Location
from src.renp_ai.game.python_code.constructs.scene import Scene
from src.renp_ai.game.python_code.constructs.character import Character
from src.renp_ai.game.python_code.ai.context_manager import ContextManager
from src.renp_ai.game.python_code.api_manager.llm_client import LLMClient
from src.renp_ai.game.python_code.api_manager.api_key_manager import APIKeyManager
from src.renp_ai.game.python_code.config import DEFAULT_MODEL, DEFAULT_MAX_TOKENS, SYSTEM_PROMPT

# Test script for the new Scene and Character functionality

if __name__ == "__main__":
    # Initialize the ContextManager with the system prompt and a seed prompt
    context_manager = ContextManager(system_prompt=SYSTEM_PROMPT, seed_prompt="Describe a mysterious forest.")

    # Create a location
    location = Location(name="Mysterious Forest", description="A dark and eerie forest.", filepath="Mysterious_Forest.png")

    # Create characters
    character1 = Character(name="The Wanderer", description="A lost soul seeking answers.")
    character2 = Character(name="The Guardian", description="A mysterious figure guarding the forest.")

    # Create a scene and add location and characters
    scene = Scene(description="A tense encounter in the heart of the forest.")
    scene.set_location(location)
    scene.set_characters([character1, character2])

    # Set the scene in the ContextManager
    context_manager.set_scene(scene)

    # Initialize the API key manager
    api_key_manager = APIKeyManager()
    api_key_manager.save_api_key("sk-your-api-key-here")  # Replace with a valid API key

    # Initialize the LLM client
    llm_client = LLMClient(context_manager=context_manager, model=DEFAULT_MODEL, max_tokens=DEFAULT_MAX_TOKENS, api_key_manager=api_key_manager)

    # Get the context with the scene and request a completion
    context = context_manager.get_context()
    response = llm_client.get_llm_response(user_message="What happens next in the scene?")

    # Print the context and response for testing
    print("Context: ", json.dumps(context, indent=2))
    print("LLM Response: ", response)

