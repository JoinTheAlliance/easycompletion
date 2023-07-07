# easycompletion

Easy function calling using OpenAI's API. Handles a lot of the annoying boilerplate. Useful if you want a clean, validated response. Simple codebase, made after many hours of frustration with the various pitfalls and instabilities of the OpenAI API.

<img src="resources/image.jpg">

# Installation

```bash
pip install easycompletion
```

# Usage

## Importing

```python
from easycompletion import openai_function_call, openai_text_call, compose_prompt
```

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
# response = "As an AI language model, I don't have feelings, but...""
```

## Function Completion

Send text and a list of functions and get a response as a function call

```python
from easycompletion import openai_function_call

# This function follows OpenAI's function schema format
# https://platform.openai.com/docs/guides/gpt/function-calling
test_function = {
    "name": "write_song",
    "description": "Write a song about AI",
    "parameters": {
        "type": "object",
        "properties": {
            "lyrics": {
                "type": "string",
                "description": "The lyrics for the song",
            }
        },
        "required": ["lyrics"],
    },
}

response = openai_function_call(text="Write a song about AI", functions=[test_function], function_call="write_song")
# Response structure is { "text": string, "function_name": string, "arguments": dict  }
print(response["arguments"]["lyrics"])
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

If you have any questions, please feel free to reach out to me on [Twitter](https://twitter.com/spatialweeb) or [Discord](@new.moon).
