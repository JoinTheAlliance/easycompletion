from .prompt import count_tokens

openai.api_base = EASYCOMPLETION_API_ENDPOINT

def parse_arguments(arguments, debug=DEBUG):
    """
    Parses arguments that are expected to be either a JSON string, dictionary, or a list.
	@@ -154,7 +168,6 @@ def validate_functions(response, functions, function_call, debug=DEBUG):
    log("Function call is valid", type="success", log=debug)
    return True

def chat_completion(
    messages,
    model_failure_retries=5,
	@@ -180,10 +193,11 @@ def chat_completion(
    Example:
        >>> text_completion("Hello, how are you?", model_failure_retries=3, model='gpt-3.5-turbo', chunk_length=1024, api_key='your_openai_api_key')
    """
    # Validate the API key
    if not validate_api_key(api_key):
        return {"error": "Invalid OpenAI API key"}

    openai.api_key = api_key

    # Use the default model if no model is specified
    if model == None:
	@@ -363,6 +377,7 @@ def function_completion(
    api_key=None,
    debug=DEBUG,
    temperature=0.0,

):
    """
    Send text and a list of functions to the model and return optional text and a function call.
	@@ -560,5 +575,40 @@ def function_completion(
        "arguments": arguments,
        "usage": usage,
        "finish_reason": finish_reason,
        "model_used": model,  # Include the model used in the response
        "error": None,
    }


def status_info(api_key=None, model=None, debug=DEBUG):
    """
    Get status information about the API key and model.
    Parameters:
        api_key (str, optional): OpenAI API key. If not provided, it uses the one defined in constants.py.
        model (str, optional): The model to use. Default is the TEXT_MODEL defined in constants.py.
    Returns:
        dict: A dictionary containing status information.
    Example:
        >>> status_info(api_key='your_openai_api_key', model='gpt-3.5-turbo')
    """
    # Validate the API key
    if not validate_api_key(api_key):
        return {"error": "Invalid OpenAI API key"}

    openai.api_key = api_key

    if model is None:
        model = TEXT_MODEL

    # Get the model information
    model_info = openai.Model.retrieve(model)
    model_status = model_info.status

    return {
        "api_key": api_key,
        "model": model,
        "model_status": model_status,
    }
