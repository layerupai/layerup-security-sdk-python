from layerup_security.config import Config
from layerup_security.utils import make_api_call
import json

class LayerupSecurity:
    """
    A Python wrapper for the Layerup Security API.
    """

    def __init__(self, api_key, base_url=None):
        """
        Initializes the LayerupSecurity object with API key and optional configuration.

        :param api_key: The API key for authenticating with the Layerup Security API.
        :param base_url: Optional custom base URL for the API. Defaults to the standard URL.
        """
        self.config = Config(api_key, base_url)

    def intercept_prompt(self, messages, metadata={}):
        """
        Intercept unsafe prompts before they are sent to an LLM.

        :param messages: List of messages in the LLM conversation.
        :param metadata: Optional metadata object for the request.
        :return: The JSON response from the API call.
        """
        url = f"{self.config.base_url}/intercept/prompt"
        headers = {"Layerup-API-Key": self.config.api_key, "Content-Type": "application/json"}
        data = {"messages": messages, "metadata": metadata}

        return make_api_call(url, method='POST', headers=headers, data=data)

    def intercept_response(self, messages, metadata={}):
        """
        Intercept unsafe LLM responses before they get to your users.

        :param messages: List of messages in the LLM conversation.
        :param metadata: Optional metadata object for the request.
        :return: The JSON response from the API call.
        """
        url = f"{self.config.base_url}/intercept/response"
        headers = {"Layerup-API-Key": self.config.api_key, "Content-Type": "application/json"}
        data = {"messages": messages, "metadata": metadata}

        return make_api_call(url, method='POST', headers=headers, data=data)

    def mask_prompt(self, messages, metadata={}):
        """
        Mask sensitive information in your prompts before sending them to an LLM.

        :param messages: List of messages in the LLM conversation.
        :param metadata: Optional metadata object for the request.
        :return: Tuple including (1) the masked messages, and (2) an unmasking function
        """
        url = f"{self.config.base_url}/mask/prompt"
        headers = {"Layerup-API-Key": self.config.api_key, "Content-Type": "application/json"}
        data = {"messages": messages, "metadata": metadata}

        masked_response = make_api_call(url, method='POST', headers=headers, data=data)

        def deep_copy_dict(dict):
            return json.loads(json.dumps(dict))

        def replace_variables(string, variables):
            for key, value in variables.items():
                string = string.replace(key, value)
            return string

        def unmask_response(templated_response):
            # If they provided the OpenAI-formatted object, then unmask the first
            # choice's message content and return a copy of the object.
            if isinstance(templated_response, dict) and templated_response['object'] == 'chat.completion':
                updated_string = replace_variables(
                    templated_response['choices'][0]['message']['content'],
                    masked_response['variables']
                )
                unmasked_result = deep_copy_dict(templated_response)
                unmasked_result['choices'][0]['message']['content'] = updated_string
                return unmasked_result

            # If they provided a raw output string, then unmask a copy of the string
            # and return it.
            elif isinstance(templated_response, str):
                unmasked_result = replace_variables(
                    templated_response,
                    masked_response['variables']
                )
                return unmasked_result

            # Otherwise, we're not sure how to handle the provided response
            else:
                raise ValueError('The unmask function takes either a chat.completion OpenAI-schema response, or a raw output string. Do not do any post-processing on the LLM response before calling the unmask function.')

        return masked_response['messages'], unmask_response

    def log_error(self, error, messages, metadata={}):
        """
        Log LLM errors in order to seamlessly view insights as to why your LLM calls are failing or timing out, trace errors, and identify patterns.

        :param error: Error from LLM for tracing and logging.
        :param messages: List of messages in the LLM conversation.
        :param metadata: Optional metadata object for the request.
        :return: The JSON response from the API call.
        """
        url = f"{self.config.base_url}/log/error"
        headers = {"Layerup-API-Key": self.config.api_key, "Content-Type": "application/json"}
        data = {"error": error, "messages": messages, "metadata": metadata}

        return make_api_call(url, method='POST', headers=headers, data=data)

    def execute_rules(self, rules, messages, metadata={}):
        """
        Execute pre-defined rules that allow you to send canned responses when a user prompts in a certain way, adding yet another layer of protection to your LLM calls.

        :param rules: List of rule names to execute.
        :param messages: List of messages in the LLM conversation.
        :param metadata: Optional metadata object for the request.
        :return: The JSON response from the API call.
        """
        url = f"{self.config.base_url}/rules/execute"
        headers = {"Layerup-API-Key": self.config.api_key, "Content-Type": "application/json"}
        data = {"rules": rules, "messages": messages, "metadata": metadata}

        return make_api_call(url, method='POST', headers=headers, data=data)