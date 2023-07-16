import os
import time
import openai
import re
import json
import ast

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .constants import (
    default_text_model,
    long_text_model,
    openai_api_key,
    default_chunk_length,
)

from .prompt import count_tokens

# Set the OpenAI API key
openai.api_key = openai_api_key


def parse_arguments(arguments):
    """
    Parses arguments that are expected to be either a JSON string, dictionary, or a list.

    Parameters:
        arguments (str or dict or list): Arguments in string or dictionary or list format.

    Returns:
        A dictionary or list of arguments if arguments are valid, None otherwise.

    Usage:
        arguments = parse_arguments('{"arg1": "value1", "arg2": "value2"}')
    """
    try:
        # Handle string inputs, remove any ellipsis from the string
        if isinstance(arguments, str):
            arguments = re.sub(r"\.\.\.|\…", "", arguments)
            return json.loads(arguments)
        # If input is already a dictionary or list, return as is
        elif isinstance(arguments, dict) or isinstance(arguments, list):
            return arguments
    # If JSON decoding fails, try using ast.literal_eval
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(arguments)
        # If ast.literal_eval fails, remove line breaks and non-ASCII characters and try JSON decoding again
        except (ValueError, SyntaxError):
            try:
                arguments = re.sub(r"[\r\n]+", "", arguments)
                arguments = re.sub(r"[^\x00-\x7F]+", "", arguments)
                return json.loads(arguments)
            # If everything fails, try Python's eval function
            except (ValueError, SyntaxError):
                try:
                    return eval(arguments)
                except (ValueError, SyntaxError):
                    return None


def validate_functions(response, functions, function_call):
    """
    Validates if the function returned by the OpenAI API matches the intended function call.

    Parameters:
        response (dict): The response from OpenAI API.
        functions (list): A list of function definitions.
        function_call (dict or str): The expected function call.

    Returns:
        True if function call matches with the response, False otherwise.

    Usage:
        isValid = validate_functions(response, functions, function_call)
    """
    # Extract the function call from the response
    response_function_call = response["choices"][0]["message"]["function_call"]

    # If function_call is not "auto" and the name does not match with the response, return False
    if (
        function_call != "auto"
        and response_function_call["name"] != function_call["name"]
    ):
        return False

    # If function_call is "auto", extract the name from the response
    function_call_name = (
        function_call["name"]
        if function_call != "auto"
        else response_function_call["name"]
    )

    # Parse the arguments from the response
    arguments = parse_arguments(response_function_call["arguments"])

    # If arguments are None, return False
    if arguments is None:
        return False

    # Get the function that matches the function name from the list of functions
    function = next(
        (item for item in functions if item["name"] == function_call_name), None
    )

    # If no matching function is found, return False
    if function is None:
        return False

    # Check if the function's argument keys match with the response's argument keys
    if set(function["parameters"]["properties"].keys()) == set(arguments.keys()):
        return True

    return False


def compose_function(name, description, properties, required_properties):
    """
    Composes a function object for OpenAI API.

    Parameters:
        name (str): The name of the function.
        description (str): Description of the function.
        properties (dict): Dictionary of property objects.
        required_properties (list): List of property names that are required.

    Returns:
        A dictionary representing a function.

    Usage:
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
    """
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required_properties,
        },
    }


def openai_text_call(
    text,
    model_failure_retries=5,
    model=None,
    chunk_length=default_chunk_length,
    api_key=None,
):
    """
    Function for sending text to the OpenAI API and returning a text response.

    Parameters:
        text (str): Text to send to the model.
        model_failure_retries (int, optional): Number of retries if the request fails. Default is 5.
        model (str, optional): The model to use. Default is the default_text_model defined in constants.py.
        chunk_length (int, optional): Maximum length of text chunk to process. Default is defined in constants.py.
        api_key (str, optional): OpenAI API key. If not provided, it uses the one defined in constants.py.

    Returns:
        str: The response content from the model.

    Example:
        >>> openai_text_call("Hello, how are you?", model_failure_retries=3, model='gpt-3.5-turbo', chunk_length=1024, api_key='your_openai_api_key')
    """

    # Override the API key if provided as parameter
    if api_key is not None:
        openai.api_key = api_key

    # Use the default model if no model is specified
    if model == None:
        model = default_text_model

    # Count tokens in the input text
    total_tokens = count_tokens(text, model=model)

    # If text is longer than chunk_length and model is not for long texts, switch to the long text model
    if total_tokens > chunk_length and "16k" not in model:
        model = long_text_model
        if not os.environ.get("SUPPRESS_WARNINGS"):
            print("Warning: Message is long. Using 16k model (to hide this message, set SUPPRESS_WARNINGS=1)")

    # If text is too long even for long text model, return None
    if total_tokens > (16384 - chunk_length):
        print("Error: Message too long")
        return {
            "text": None,
            usage: None,
            "finish_reason": None,
            "error": "Message too long",
        }

    # Prepare messages for the API call
    messages = [{"role": "user", "content": text}]

    # Try making a request to the OpenAI API
    def try_request():
        try:
            return openai.ChatCompletion.create(model=model, messages=messages)
        except Exception as e:
            return None

    # Try to make a request for a specified number of times
    response = None
    for i in range(model_failure_retries):
        response = try_request()
        if response:
            break
        # wait 1 second
        time.sleep(1)

    # If response is not valid, print an error message and return None
    if (
        response is None
        or response["choices"] is None
        or response["choices"][0] is None
    ):
        return {
            "text": None,
            usage: None,
            "finish_reason": None,
            "error": "Error: Could not get a successful response from OpenAI API",
        }

    # Extract content from the response
    text = response["choices"][0]["message"]["content"]
    finish_reason = response["choices"][0]["finish_reason"]
    usage = response["usage"]

    return {
        "text": text,
        "usage": usage,
        "finish_reason": finish_reason,
        "error": None,
    }


def openai_function_call(
    text,
    functions=None,
    model_failure_retries=5,
    function_call=None,
    function_failure_retries=10,
    chunk_length=default_chunk_length,
    model=None,
    api_key=None,
):
    """
    Send text and a list of functions to the OpenAI API and return optional text and a function call.
    The function call is validated against the functions array.
    The input text is sent to the chat model and is treated as a user message.

    Args:
        text (str): Text that will be sent as the user message to the model.
        functions (list[dict] | dict | None): List of functions or a single function dictionary to be sent to the model.
        model_failure_retries (int): Number of times to retry the request if it fails (default is 5).
        function_call (str | dict | None): 'auto' to let the model decide, or a function name or a dictionary containing the function name (default is "auto").
        function_failure_retries (int): Number of times to retry the request if the function call is invalid (default is 10).
        chunk_length (int): The length of each chunk to be processed.
        model (str | None): The model to use (default is the default_text_model, i.e. gpt-3.5-turbo).
        api_key (str | None): If you'd like to pass in a key to override the environment variable OPENAI_API_KEY.

    Returns:
        dict: On most errors, returns a dictionary with an "error" key. On success, returns a dictionary containing
        "text" (response from the model), "function_name" (name of the function called), "arguments" (arguments for the function), "error" (None).

    Example:
        >>> function = {'name': 'function1', 'parameters': {'param1': 'value1'}}
        >>> openai_function_call("Call the function.", function)
    """

    # Check if the user provided an API key
    if api_key is not None:
        openai.api_key = api_key

    # Ensure that functions are provided
    if functions is None:
        return {"error": "functions is required"}

    # Check if a list of functions is provided
    if not isinstance(functions, list):
        if (
            isinstance(functions, dict)
            and "name" in functions
            and "parameters" in functions
        ):
            # A single function is provided as a dictionary, convert it to a list
            functions = [functions]
        else:
            # Functions must be either a list of dictionaries or a single dictionary
            return {
                "error": "functions must be a list of functions or a single function"
            }

    # Set the function call to the name of the function if only one function is provided
    # If there are multiple functions, use "auto"
    if function_call is None:
        function_call = functions[0]["name"] if len(functions) == 1 else "auto"

    # Make sure text is provided
    if text is None:
        return {"error": "text is required"}

    # Check if the function call is valid
    if function_call != "auto":
        if isinstance(function_call, str):
            function_call = {"name": function_call}
        elif "name" not in function_call:
            return {
                "error": "function_call had an invalid name. Should be a string of the function name or an object with a name property"
            }

    # Use the default text model if no model is specified
    if model is None:
        model = default_text_model

    # Count the number of tokens in the message
    message_tokens = count_tokens(text, model=model)
    total_tokens = message_tokens

    if functions is None:
        function_call_tokens = count_tokens(functions, model=model)
        total_tokens += function_call_tokens + 3  # Additional tokens for the user

    # Switch to a larger model if the message is too long for the default model
    if total_tokens > chunk_length and "16k" not in model:
        model = long_text_model
        if not os.environ.get("SUPPRESS_WARNINGS"):
            print("Warning: Message is long. Using 16k model (to hide this message, set SUPPRESS_WARNINGS=1)")

    # Check if the total number of tokens exceeds the maximum allowable tokens for the model
    if total_tokens > (16384 - chunk_length):
        return {"error": "Message too long"}

    # Prepare the messages to be sent to the API
    messages = [{"role": "user", "content": text}]

    # Define a nested function to handle API request and exceptions
    def try_request():
        """Attempts to create a chat completion with OpenAI's API and handles any exceptions that may occur."""
        try:
            # If there are function(s) to call
            if functions:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    functions=functions,
                    function_call=function_call,
                )
            else:
                # If there are no function(s) to call
                response = openai.ChatCompletion.create(model=model, messages=messages)
            return response
        except Exception as e:
            print(f"OpenAI Error: {e}")
            return None

    # Retry function call and model calls according to the specified retry counts
    response = None
    for _ in range(function_failure_retries):
        for _ in range(model_failure_retries):
            response = try_request()
            if response:
                break
        if functions is None or validate_functions(response, functions, function_call):
            break

    # Check if we have a valid response from OpenAI API
    if (
        response is None
        or not response.get("choices")
        or response["choices"][0] is None
    ):
        error = "Could not get a successful response from OpenAI API"
        print(error)
        return {"error": error}

    # Extracting the content and function call response from API response
    response_data = response["choices"][0]["message"]
    finish_reason = response["choices"][0]["finish_reason"]
    usage = response["usage"]

    text = response_data["content"]
    function_call_response = response_data.get("function_call", None)

    # If no function call in response, return an error
    if function_call_response is None:
        return {"error": "No function call in response"}

    # Return the final result with the text response, function name, arguments and no error
    return {
        "text": text,
        "function_name": function_call_response["name"],
        "arguments": parse_arguments(function_call_response["arguments"]),
        "usage": usage,
        "finish_reason": finish_reason,
        "error": None,
    }
