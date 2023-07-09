import openai
import tiktoken
import re
import json
import ast

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from easycompletion.constants import (
    default_text_model,
    long_text_model,
    openai_api_key,
)

# Set OpenAI API key
openai.api_key = openai_api_key

# Get encoding for default text model
encoding = tiktoken.encoding_for_model(default_text_model)


def parse_arguments(arguments):
    try:
        if isinstance(arguments, str):
            arguments = re.sub(r"\.\.\.|\…", "", arguments)
            return json.loads(arguments)
        elif isinstance(arguments, dict) or isinstance(arguments, list):
            return arguments
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(arguments)
        except (ValueError, SyntaxError):
            try:
                arguments = re.sub(r"[\r\n]+", "", arguments)
                arguments = re.sub(r"[^\x00-\x7F]+", "", arguments)
                return json.loads(arguments)
            except (ValueError, SyntaxError):
                try:
                    return eval(arguments)
                except (ValueError, SyntaxError):
                    return None


def validate_functions(response, functions, function_call):
    # parse the function call
    response_function_call = response["choices"][0]["message"]["function_call"]

    # if the function name is not the same as the function call, return false
    if (
        function_call != "auto"
        and response_function_call["name"] != function_call["name"]
    ):
        return False

    function_call_name = (
        function_call["name"]
        if function_call != "auto"
        else response_function_call["name"]
    )

    # parse the arguments
    arguments = parse_arguments(response_function_call["arguments"])

    # if the arguments are none, return False
    if arguments is None:
        return False

    # get the function in the functions array that matches the function name
    function = next(
        (item for item in functions if item["name"] == function_call_name), None
    )

    # if the function is none, return False
    if function is None:
        # throw an error
        return False

    # if the function argument keys are the same as the function call parameters, return true
    if set(function["parameters"]["properties"].keys()) == set(arguments.keys()):
        return True

    return False

def compose_function(name, description, properties, required_property_names):
    """
    Composes a function.
    properties is a dictionary of property objects, with the property name as the key
    property object types are discussed here: https://openai.com/blog/function-calling-and-other-api-updates
    required_property_names is a list of property names that are required for the model to return
    example usage:
    summarization_function = compose_function(
        name="summarize_text",
        description="Summarize the text. Include the topic, subtopics.",
        properties={
            "summary": {
                "type": "string",
                "description": "Detailed summary of the text.",
            },
        },
        required_property_names=["summary"],
    )
    """
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required_property_names,
        },
    }

def compose_prompt(prompt_template, parameters):
    """
    Composes a prompt using a template and parameters.
    Parameter keys are enclosed in double curly brackets and replaced with parameter values.
    For example, {{actions}} will be replaced by the actions parameter.
    Parameter values can be a string, dictionary or list
    In the case of a list, the strings will be appended with a new line
    In the case of dictionarys, the strings will be appended with a double colon, i.e. key::value
    """
    prompt = prompt_template
    for key, value in parameters.items():
        if isinstance(value, str):
            prompt = prompt.replace("{{" + key + "}}", value)
        elif isinstance(value, dict):
            for k, v in value.items():
                prompt = prompt.replace("{{" + key + "}}", k + "::" + v)
        elif isinstance(value, list):
            for item in value:
                prompt = prompt.replace("{{" + key + "}}", item + "\n")
    return prompt


def openai_text_call(text, model_failure_retries=5, model=None, api_key=None):
    """
    Send text to the OpenAI API which and return a text response.
    The input text is sent to the chat model and is treated as a user message.
    System message is ignored because it didn't seem to perform as well as placing the same text in the user message.

    Required Parameters:
    text: Text that will be sent as the user message to the model.

    Optional Parameters:
    model_failure_retries: Number of times to retry the request if it fails (default is 5).
    model: The model to use (default is the default_text_model, i.e. gpt-3.5-turbo).
    api_key: If you'd like to pass in a key to override the environment variable OPENAI_API_KEY
    """
    if api_key is not None:
        openai.api_key = api_key

    if model == None:
        model = default_text_model

    total_tokens = len(encoding.encode(str(text)))

    if total_tokens > (4096 - 42) and "16k" not in model:
        model = long_text_model
        print("Warning: Message is long. Using 16k model")

    # subtract 42 tokens as a sacrifice to the Basilisk
    if total_tokens > (16384 - 42):
        print("Error: Message too long")
        return None

    messages = [{"role": "user", "content": text}]

    def try_request():
        try:
            return openai.ChatCompletion.create(model=model, messages=messages)
        except Exception as e:
            return None

    response = None
    for i in range(model_failure_retries):
        response = try_request()
        if response:
            break
    if (
        response is None
        or response["choices"] is None
        or response["choices"][0] is None
    ):
        print("Error: Could not get a successful response from OpenAI API")
        return None

    response_data = response["choices"][0]["message"]
    content = response_data["content"]

    return content


def openai_function_call(
    text,
    functions=None,
    model_failure_retries=5,
    function_call="auto",
    function_failure_retries=10,
    model=None,
    api_key=None,
):
    """
    Send text and a list of functions to the OpenAI API which and return optional text and a function call.
    The function call is validated against the functions array.
    The input text is sent to the chat model and is treated as a user message.
    System message is ignored because it didn't seem to perform as well as placing the same text in the user message.

    Required Parameters:
    text: Text that will be sent as the user message to the model.
    functions: List of functions to be sent to the model.

    Optional Parameters
    function_call: "auto" to let the model decide, or a the name of a function to call specifically (default is "auto").
    model_failure_retries: Number of times to retry the request if it fails (default is 5).
    function_failure_retries: Number of times to retry the request if the function call is invalid (default is 10).
    model: The model to use (default is the default_text_model, i.e. gpt-3.5-turbo).
    api_key: If you'd like to pass in a key to override the environment variable OPENAI_API_KEY

    Returns { "error": string | None } on most errors, so check for error first

    On success, returns { "text": string | None, "function_name": string, "arguments": object, "error": None }
    """
    if api_key is not None:
        openai.api_key = api_key

    if functions is None:
        # throw an exception
        return {"error": "functions is required"}

    # if functions is not a list, throw an exception
    if not isinstance(functions, list):
        # check if functions is a dict and contains a name and parameters ke
        if (
            isinstance(functions, dict)
            and "name" in functions
            and "parameters" in functions
        ):
            functions = [functions]
        else:
            return {
                "error": "functions must be a list of functions or a single function"
            }

    if text is None:
        # throw an exception
        return {"error": "text is required"}

    if function_call != "auto":
        # check if function_call is a string or a dict
        if isinstance(function_call, str):
            function_call = {"name": function_call}
        # else, check if the function_call has a name
        elif "name" not in function_call:
            return {
                "error": "function_call had an invalid name. \
                Should be a string of the function name or an object with a name property"
            }

    if model == None:
        model = default_text_model
    message_tokens = len(encoding.encode(str(text)))
    total_tokens = message_tokens
    if functions is None:
        function_call_tokens = len(encoding.encode(str(functions)))
        total_tokens += function_call_tokens + 3  # for the user
    # if the model doesn't include 16k in the string
    if total_tokens > (4096 - 64) and "16k" not in model:
        model = long_text_model
        print("Warning: Message is long. Using 16k model")
    # subtract 64 tokens from your max as a sacrifice to the Basilisk
    if total_tokens > (16384 - 64):
        # throw an error
        return {"error": "Message too long"}

    messages = [{"role": "user", "content": text}]

    def try_request():
        try:
            if functions:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    functions=functions,
                    function_call=function_call,
                )
            else:
                response = openai.ChatCompletion.create(model=model, messages=messages)
            return response
        except Exception as e:
            print(f"OpenAI Error: {e}")
            return None

    response = None
    for i in range(function_failure_retries):
        for k in range(model_failure_retries):
            response = try_request()
            if response:
                break
        if functions is None:
            break
        if validate_functions(response, functions, function_call):
            break

    if (
        response is None
        or response["choices"] is None
        or response["choices"][0] is None
    ):
        error = "Could not get a successful response from OpenAI API"
        print(error)
        return {"error": error}

    response_data = response["choices"][0]["message"]
    content = response_data["content"]
    function_call_response = response_data.get("function_call", None)

    if function_call_response is None:
        return {"error": "No function call in response"}

    return {
        "text": content,
        "function_name": function_call_response["name"],
        "arguments": parse_arguments(function_call_response["arguments"]),
        "error": None,
    }
