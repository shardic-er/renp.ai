class APIKeyManager:
    def __init__(self):
        self.api_key = persistent.api_key if hasattr(persistent, 'api_key') else None

    def save_api_key(self, key):
        self.api_key = key
        persistent.api_key = key
        renpy.save_persistent()  # Ensure the persistent data is saved immediately

    def validate_api_key(self, llm_client):
        test_response = llm_client.get_llm_response("Hello!")
        return test_response is not None
