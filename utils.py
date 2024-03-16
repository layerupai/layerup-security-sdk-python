import requests

def make_api_call(url, method='GET', headers=None, params=None, data=None):
    """
    Generic function to make API calls to the Layerup Security API.
    
    :param url: The full URL to make the request to.
    :param method: The HTTP method to use for the request. Defaults to 'GET'.
    :param headers: Optional headers to include in the request.
    :param params: Optional URL parameters to append to the URL.
    :param data: Optional data to send in the body of the request.
    :return: The JSON response from the API call.
    """
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, params=params, json=data)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, params=params, json=data)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, params=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status() # Raises a HTTPError if the response status code is 4XX/5XX
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API call: {e}")
        return None