# Layerup Security Python SDK

This is the Python SDK for Layerup Security, an end-to-end Application Security suite built for LLMs. Get started by creating an account on [our dashboard](https://dashboard.uselayerup.com) and following the instructions below.

## Installation

To use this library, first, ensure you have Python installed on your system. Then, clone this repository and install:

```
pip install LayerupSecurity
```

### API Key

Grab your API key from [our dashboard](https://dashboard.uselayerup.com) and add it to your project environment as `LAYERUP_API_KEY`.

### Import and Configure

```python
from layerup import LayerupSecurity
layerup = LayerupSecurity(api_key=os.getenv('LAYERUP_API_KEY'))
```

### Execute Guardrails

Execute pre-defined guardrails that allow you to send canned responses when a user prompts in a certain way, adding a layer of protection to your LLM calls.

```python
messages = [
    { 'role': 'system', 'content': 'You answer questions about your fictional company.' },
    { 'role': 'user', 'content': 'Can I get a 15% discount?' },
]

# Make the call to Layerup
security_response = layerup.execute_guardrails(
    ['layerup.security.prompt.discount'],
    messages
)

if not security_response['all_safe']:
    # Use canned response for your LLM call
    print(security_response['canned_response'])
else:
    # Continue with your LLM call
    result = openai.ChatCompletion.create(
        messages=messages,
        model='gpt-3.5-turbo',
    )
```

### Mask Prompts

Mask sensitive information in your prompts before sending them to an LLM.

```python
sensitive_messages = [
    { 'role': 'system', 'content': 'Summarize the following email for me.' },
    { 'role': 'user', 'content': 'Dear Mr. Smith, hope you are doing well. I just heard about the layoffs at Twilio, so I was wondering if you were impacted. Can you please call me back at your earliest convenience? My number is (123) 456-7890. Best Regards, Bob Dylan' },
]

# Make the call to Layerup
messages, unmask_response = layerup.mask_prompt(sensitive_messages)

# Call OpenAI using the masked messages from Layerup
result = openai.ChatCompletion.create(
    messages=messages,
    model='gpt-3.5-turbo',
)

# Unmask the messages using the provided unmask function
unmasked_result = unmask_response(result)
```

### Log Errors

Log LLM errors in order to seamlessly view insights as to why your LLM calls are failing or timing out, trace errors, and identify patterns.

```python
messages = [
    {'role': 'system', 'content': 'You are Jedi master Yoda.'},
    {'role': 'user', 'content': "What is Luke Skywalker's favorite fruit?"},
]

try:
    # Send your request
    openai.ChatCompletion.create(
        messages=messages,
        model='gpt-3.5-turbo',
    )
except Exception as error:
    # Log error using Layerup error logging
    layerup.log_error(str(error), messages)
```
