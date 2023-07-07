import openai
import tiktoken
import re
import json
import ast

from constants import (
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
    response_function_call = response["choices"][0]["function_call"]

    # if the function name is not the same as the function call, return false
    if response_function_call["name"] != function_call["name"]:
        print("Function name does not match")
        return False

    # parse the arguments
    arguments = parse_arguments(response_function_call["arguments"])

    # if the arguments are none, return False
    if arguments is None:
        print("Arguments are none")
        return False

    # get the function in the functions array that matches the function name
    function = next(
        (item for item in functions if item["name"] == function_call["name"]), None
    )

    # if the function is none, return False
    if function is None:
        print("Function could not be found")
        # throw an error
        return False

    # if the function argument keys are the same as the function call parameters, return true
    if set(function["parameters"]["properties"].keys()) == set(arguments.keys()):
        return True

    print("Function argument keys are not the same as the function call parameters")
    # print the keys and properties
    print(set(function["parameters"]["properties"].keys()))
    print(set(arguments.keys()))
    return False


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


def use_language_model(
    message,
    functions=None,
    model_failure_retries=5,
    function_call="auto",
    require_function=True,
    function_failure_retries=10,
):
    """
    Creates a chat completion using OpenAI API and writes the completion to a log file.

    Parameters:
    messages: List of message objects to be sent to the chat model.
    actions: List of action calls to be sent to the chat model (Optional).

    Returns:
    { "text": string, "function_call": { "name": string, "arguments": object }
    """

    model = default_text_model
    message_tokens = len(encoding.encode(str(message)))
    function_call_tokens = len(encoding.encode(str(functions)))

    total_tokens = message_tokens + function_call_tokens + 3  # for the user
    # if the model doesn't include 16k in the string
    if total_tokens > 4096 and "16k" not in model:
        model = long_text_model
        print("Warning: Message is long. Using 16k model")
    if total_tokens > 16384:
        # throw an error
        return {"error": "Message too long"}

    messages = [{"role": "user", "content": message}]

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
        if functions is None or require_function is False:
            break
        if validate_functions(
            response["choices"][0]["function_call"], functions, function_call
        ):
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
        function_call = None
    else:
        function_call = {
            "name": function_call_response["name"],
            "arguments": parse_arguments(function_call_response["arguments"]),
        }

    return {"text": content, "function_call": function_call, "error": None}
