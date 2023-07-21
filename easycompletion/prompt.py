import re
import tiktoken

from .constants import DEFAULT_TEXT_MODEL, DEFAULT_CHUNK_LENGTH, DEBUG
from .logger import log

def trim_prompt(
    text,
    max_tokens=DEFAULT_CHUNK_LENGTH,
    model=DEFAULT_TEXT_MODEL,
    preserve_top=True,
    debug=DEBUG,
):
    """
    Trim the given text to a maximum number of tokens.

    Args:
        text: Input text which needs to be trimmed.
        max_tokens: Maximum number of tokens allowed in the trimmed text.
                    Default value is taken from the constants.
        model: The model to use for tokenization.
        preserve_top: If True, the function will keep the first 'max_tokens' tokens,
                      if False, it will keep the last 'max_tokens' tokens.

    Returns:
        Trimmed text that fits within the specified token limit.

    Example:
        trim_prompt("This is a test.", 3, preserve_top=True)
        Output: "This is"
    """
    # Encoding the text into tokens.
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text  # If text is already within limit, return as is.
    
    log(f"Trimming prompt, token len is {str(len(tokens))}", type="warning", log=debug)

    # If 'preserve_top' is True, keep the first 'max_tokens' tokens.
    # Otherwise, keep the last 'max_tokens' tokens.
    return encoding.decode(
        tokens[:max_tokens] if preserve_top else tokens[-max_tokens:]
    )


def chunk_prompt(prompt, chunk_length=DEFAULT_CHUNK_LENGTH, debug=DEBUG):
    """
    Split the given prompt into chunks where each chunk has a maximum number of tokens.

    Args:
        prompt: Input text that needs to be split.
        chunk_length: Maximum number of tokens allowed per chunk.
                      Default value is taken from the constants.

    Returns:
        A list of string chunks where each chunk is within the specified token limit.

    Example:
        chunk_prompt("This is a test. I am writing a function.", 4)
        Output: ['This is', 'a test.', 'I am', 'writing a', 'function.']
    """
    if count_tokens(prompt) <= chunk_length:
        return [prompt]

    # Splitting the prompt into sentences using regular expressions.
    sentences = re.split(r"(?<=[.!?])\s+", prompt)
    current_chunk = ""
    prompt_chunks = []

    # For each sentence in the input text.
    for sentence in sentences:
        # If adding a new sentence doesn't exceed the token limit, add it to the current chunk.
        if count_tokens(current_chunk + sentence + " ") <= chunk_length:
            current_chunk += sentence + " "
        else:
            # If adding a new sentence exceeds the token limit, add the current chunk to the list.
            # Then, start a new chunk with the current sentence.
            prompt_chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    # If there's any sentence left after looping through all sentences, add it to the list.
    if current_chunk:
        prompt_chunks.append(current_chunk.strip())

    log(f"Chunked prompt into {str(len(prompt_chunks))} chunks", type="warning", log=debug)

    return prompt_chunks


def count_tokens(prompt: str, model=DEFAULT_TEXT_MODEL) -> int:
    """
    Count the number of tokens in a string.

    Args:
        prompt: The string to be tokenized.
        model: The model to use for tokenization.

    Returns:
        The number of tokens in the input string.

    Example:
        count_tokens("This is a test.")
        Output: 5
    """
    if not isinstance(prompt, str):
        prompt = str(prompt)
        
    encoding = tiktoken.encoding_for_model(model)
    length = len(
        encoding.encode(prompt)
    )  # Encoding the text into tokens and counting the number of tokens.
    return length


def get_tokens(prompt: str, model=DEFAULT_TEXT_MODEL) -> list:
    """
    Returns a list of tokens in a string.

    Args:
        prompt: The string to be tokenized.
        model: The model to use for tokenization.

    Returns:
        A list of tokens in the input string.

    Example:
        get_tokens("This is a test.")
        Output: [This, is, a, test, .]
    """
    encoding = tiktoken.encoding_for_model(model)
    return encoding.encode(
        prompt
    )  # Encoding the text into tokens and returning the list of tokens.


def compose_prompt(prompt_template, parameters, debug=DEBUG):
    """
    Composes a prompt using a template and parameters.
    Parameter keys are enclosed in double curly brackets and replaced with parameter values.

    Args:
        prompt_template: A template string that contains placeholders for the parameters.
        parameters: A dictionary containing key-value pairs to replace the placeholders.

    Returns:
        A string where all placeholders have been replaced with actual values from the parameters.

    Example:
        compose_prompt("Hello {{name}}!", {"name": "John"})
        Output: "Hello John!"
    """
    prompt = prompt_template  # Initial prompt template.

    # Replacing placeholders in the template with the actual values from the parameters.
    for key, value in parameters.items():
        # check if "{{" + key + "}}" is in prompt
        # if not, continue
        if "{{" + key + "}}" not in prompt:
            continue
        try:
            if isinstance(value, str):
                prompt = prompt.replace("{{" + key + "}}", value)
            elif isinstance(value, int):
                prompt = prompt.replace("{{" + key + "}}", str(value))
            elif isinstance(value, dict):
                for k, v in value.items():
                    prompt = prompt.replace("{{" + key + "}}", k + "::" + v)
            elif isinstance(value, list):
                for item in value:
                    prompt = prompt.replace("{{" + key + "}}", item + "\n")
            elif value is None:
                prompt = prompt.replace("{{" + key + "}}", "None")
            else:
                raise Exception(f"ERROR PARSING:\n{key}\n{value}")
        except:
            raise Exception(f"ERROR PARSING:\n{key}\n{value}")

    log(f"Composed prompt:\n{prompt}", log=debug)

    return prompt
