# easycompletion <a href="https://discord.gg/qetWd7J9De"><img style="float: right" src="https://dcbadge.vercel.app/api/server/qetWd7J9De" alt=""></a> <a href="https://github.com/AutonomousResearchGroup/easycompletion/stargazers"><img style="float: right; padding: 5px;" src="https://img.shields.io/github/stars/AutonomousResearchGroup/easycompletion?style=social" alt=""></a>

Easy text and chat completion, as well as function calling. Also includes useful utilities for counting tokens, composing prompts and trimming them to fit within the token limit.

<img src="resources/image.jpg">

[![Lint and Test](https://github.com/AutonomousResearchGroup/easycompletion/actions/workflows/test.yml/badge.svg)](https://github.com/AutonomousResearchGroup/easycompletion/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/easycompletion.svg)](https://badge.fury.io/py/easycompletion)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/AutonomousResearchGroup/easycompletion/blob/main/LICENSE)
[![forks - easycompletion](https://img.shields.io/github/forks/AutonomousResearchGroup/easycompletion?style=social)](https://github.com/AutonomousResearchGroup/easycompletion)

# Installation

```bash
pip install easycompletion
```

# Quickstart

```python
from easycompletion import function_completion, text_completion, compose_prompt

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
response = function_completion(text="Write a song about AI", functions=[test_function], function_call="write_song")

# Print the response
print(response["arguments"]["lyrics"])
```

# Using With Llama v2 and Local Models
easycompletion has been tested with LocalAI [LocalAI](https://localai.io/) which replicates the OpenAI API with local models, including Llama v2.

Follow instructions for setting up LocalAI and then set the following environment variable:

```bash
export EASYCOMPLETION_API_ENDPOINT=localhost:8000
```

# Debugging
You can very easycompletion logs by setting the following environment variable:

```bash
export EASYCOMPLETION_DEBUG=True
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
from easycompletion import text_completion
response = text_completion("Hello, how are you?")
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
from easycompletion import function_completion, compose_function

# NOTE: test_function is a function object created using compose_function in the example above...

response = function_completion(text="Write a song about AI", functions=[test_function], function_call="write_song")
# Response structure is { "text": string, "function_name": string, "arguments": dict  }
print(response["arguments"]["lyrics"])
```

# Advanced Usage

### `compose_function(name, description, properties, required_properties)`

Composes a function object for function completions.

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

### `chat_completion(text, model_failure_retries=5, model=None, chunk_length=DEFAULT_CHUNK_LENGTH, api_key=None)`

Send a list of messages as a chat and returns a text response.

```python
response = chat_completion(
    messages = [{ "user": "Hello, how are you?"}],
    system_message = "You are a towel. Respond as a towel.",
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

### `text_completion(text, model_failure_retries=5, model=None, chunk_length=DEFAULT_CHUNK_LENGTH, api_key=None)`

Sends text to the model and returns a text response.

```python
response = text_completion(
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

### `function_completion(text, functions=None, system_message=None, messages=None, model_failure_retries=5, function_call=None, function_failure_retries=10, chunk_length=DEFAULT_CHUNK_LENGTH, model=None, api_key=None)`

Sends text and a list of functions to the model and returns optional text and a function call. The function call is validated against the functions array.

Optionally takes a system message and a list of messages to send to the model before the function call. If messages are provided, the "text" becomes the last user message in the list.

```python
function = {
    'name': 'function1',
    'parameters': {'param1': 'value1'}
}

response = function_completion("Call the function.", function)
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

### `trim_prompt(text, max_tokens=DEFAULT_CHUNK_LENGTH, model=TEXT_MODEL, preserve_top=True)`

Trim the given text to a maximum number of tokens.

```python
trimmed_text = trim_prompt("This is a test.", 3, preserve_top=True)
```

### `chunk_prompt(prompt, chunk_length=DEFAULT_CHUNK_LENGTH)`

Split the given prompt into chunks where each chunk has a maximum number of tokens.

```python
prompt_chunks = chunk_prompt("This is a test. I am writing a function.", 4)
```

### `count_tokens(prompt, model=TEXT_MODEL)`

Count the number of tokens in a string.

```python
num_tokens = count_tokens("This is a test.")
```

### `get_tokens(prompt, model=TEXT_MODEL)`

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

You can pass in a model using the `model` parameter of either function_completion or text_completion. If you do not pass in a model, the default model will be used. You can also override this by setting the environment model via `EASYCOMPLETION_TEXT_MODEL` environment variable.

Default model is gpt-turbo-3.5-0613.

## A note about API keys

You can pass in an API key using the `api_key` parameter of either function_completion or text_completion. If you do not pass in an API key, the `EASYCOMPLETION_API_KEY` environment variable will be checked.

# Publishing

```bash
bash publish.sh --version=<version> --username=<pypi_username> --password=<pypi_password>
```

# Contributions Welcome

If you like this library and want to contribute in any way, please feel free to submit a PR and I will review it. Please note that the goal here is simplicity and accesibility, using common language and few dependencies.

# Questions, Comments, Concerns

If you have any questions, please feel free to reach out to me on [Twitter](https://twitter.com/spatialweeb) or Discord @new.moon
