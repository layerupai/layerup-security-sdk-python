class Config:
    """
    Configuration class for LayerupSecurity API.
    """
    # Default configuration values
    DEFAULT_BASE_URL = "https://api.uselayerup.com/v1"

    def __init__(self, api_key, base_url=None):
        """
        Initialize the configuration with the API key and optional parameters.

        :param api_key: The API key for authenticating with the Layerup Security API.
        :param base_url: Optional custom base URL for the API. Defaults to the standard URL.
        """
        self.api_key = api_key
        self.base_url = base_url if base_url is not None else self.DEFAULT_BASE_URL
