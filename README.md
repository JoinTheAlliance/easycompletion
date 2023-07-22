# easycompletion <a href="https://discord.gg/qetWd7J9De"><img style="float: right" src="https://dcbadge.vercel.app/api/server/qetWd7J9De" alt=""></a>

Easy text completion and function calling using the OpenAI API. Also includes useful utilities for counting tokens, composing prompts and trimming them to fit within the token limit.

<img src="resources/image.jpg">

# Installation

```bash
pip install easycompletion
```

# Quickstart

```python
from easycompletion import openai_function_call, openai_text_call, compose_prompt

# Compose a function object
test_function = compose_function(
    name="write_song",
    description="Write a song about AI",
    properties={
            "lyrics": {
                "type": "string",
                "description": "The lyrics for the song",
            }
    },
    required_properties: ["lyrics"],
)

# Call the function
response = openai_function_call(text="Write a song about AI", functions=[test_function], function_call="write_song")

# Print the response
print(response["arguments"]["lyrics"])
```

# Basic Usage

## Compose Prompt

You can compose a prompt using {{handlebars}} syntax

```python
test_prompt = "Don't forget your {{object}}"
test_dict = {"object": "towel"}
prompt = compose_prompt(test_prompt, test_dict)
# prompt = "Don't forget your towel"
```

## Text Completion

Send text, get a response as a text string

```python
from easycompletion import openai_text_call
response = openai_text_call("Hello, how are you?")
# response["text"] = "As an AI language model, I don't have feelings, but...""
```

## Compose a Function

Compose a function to pass into the function calling API

```python
from easycompletion import compose_function

test_function = compose_function(
    name="write_song",
    description="Write a song about AI",
    properties={
            "lyrics": {
                "type": "string",
                "description": "The lyrics for the song",
            }
    },
    required_properties: ["lyrics"],
)
```

## Function Completion

Send text and a list of functions and get a response as a function call

```python
from easycompletion import openai_function_call, compose_function

# NOTE: test_function is a function object created using compose_function in the example above...

response = openai_function_call(text="Write a song about AI", functions=[test_function], function_call="write_song")
# Response structure is { "text": string, "function_name": string, "arguments": dict  }
print(response["arguments"]["lyrics"])
```

# Advanced Usage

### `compose_function(name, description, properties, required_properties)`

Composes a function object for OpenAI API.

```python
summarization_function = compose_function(
    name="summarize_text",
    description="Summarize the text. Include the topic, subtopics.",
    properties={
        "summary": {
            "type": "string",
            "description": "Detailed summary of the text.",
        },
    },
    required_properties=["summary"],
)
```

### `openai_text_call(text, model_failure_retries=5, model=None, chunk_length=DEFAULT_CHUNK_LENGTH, api_key=None)`

Sends text to the OpenAI API and returns a text response.

```python
response = openai_text_call(
    "Hello, how are you?",
    model_failure_retries=3,
    model='gpt-3.5-turbo',
    chunk_length=1024,
    api_key='your_openai_api_key'
)
```

The response object looks like this:

```json
{
    "text": "string",
    "usage": {
        "prompt_tokens": "number",
        "completion_tokens": "number",
        "total_tokens": "number"
    },
    "error": "string|None",
    "finish_reason": "string"
}
```

### `openai_function_call(text, functions=None, model_failure_retries=5, function_call=None, function_failure_retries=10, chunk_length=DEFAULT_CHUNK_LENGTH, model=None, api_key=None)`

Sends text and a list of functions to the OpenAI API and returns optional text and a function call. The function call is validated against the functions array.

```python
function = {
    'name': 'function1',
    'parameters': {'param1': 'value1'}
}

response = openai_function_call("Call the function.", function)
```

The response object looks like this:

```json
{
    "text": "string",
    "function_name": "string",
    "arguments": "dict",
    "usage": {
        "prompt_tokens": "number",
        "completion_tokens": "number",
        "total_tokens": "number"
    },
    "finish_reason": "string",
    "error": "string|None"
}
```

### `trim_prompt(text, max_tokens=DEFAULT_CHUNK_LENGTH, model=DEFAULT_TEXT_MODEL, preserve_top=True)`

Trim the given text to a maximum number of tokens.

```python
trimmed_text = trim_prompt("This is a test.", 3, preserve_top=True)
```

### `chunk_prompt(prompt, chunk_length=DEFAULT_CHUNK_LENGTH)`

Split the given prompt into chunks where each chunk has a maximum number of tokens.

```python
prompt_chunks = chunk_prompt("This is a test. I am writing a function.", 4)
```

### `count_tokens(prompt, model=DEFAULT_TEXT_MODEL)`

Count the number of tokens in a string.

```python
num_tokens = count_tokens("This is a test.")
```

### `get_tokens(prompt, model=DEFAULT_TEXT_MODEL)`

Returns a list of tokens in a string.

```python
tokens = get_tokens("This is a test.")
```

### `compose_prompt(prompt_template, parameters)`

Composes a prompt using a template and parameters. Parameter keys are enclosed in double curly brackets and replaced with parameter values.

```python
prompt = compose_prompt("Hello {{name}}!", {"name": "John"})
```

## A note about models

You can pass in a model using the `model` parameter of either openai_function_call or openai_text_call. If you do not pass in a model, the default model will be used. You can also override this by setting the environment model via `OPENAI_MODEL` environment variable.

Default model is gpt-turbo-3.5-0613.

## A note about API keys

You can pass in an API key using the `api_key` parameter of either openai_function_call or openai_text_call. If you do not pass in an API key, the `OPENAI_API_KEY` environment variable will be checked.

# Publishing

```bash
bash publish.sh --version=<version> --username=<pypi_username> --password=<pypi_password>
```

# Contributions Welcome

If you like this library and want to contribute in any way, please feel free to submit a PR and I will review it. Please note that the goal here is simplicity and accesibility, using common language and few dependencies.

# Questions, Comments, Concerns

If you have any questions, please feel free to reach out to me on [Twitter](https://twitter.com/spatialweeb) or Discord @new.moon
