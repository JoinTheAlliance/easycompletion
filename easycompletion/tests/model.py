from easycompletion.model import (
    chat_completion,
    parse_arguments,
    function_completion,
    function_completion_async,
    text_completion,
    text_completion_async,
)
import pytest


def test_parse_arguments():
    test_input = '{"key1": "value1", "key2": 2}'
    expected_output = {"key1": "value1", "key2": 2}
    assert parse_arguments(test_input) == expected_output, "Test parse_arguments failed"

@pytest.mark.asyncio
async def test_text_completion_async():
    response = await text_completion_async("Hello, how are you?")
    assert response is not None, "Test text_completion_async failed"
    assert response["text"] is not None, "Test text_completion_async failed"
    prompt_tokens = response["usage"]["prompt_tokens"]
    assert prompt_tokens == 13, "Prompt tokens was not the expected count"


@pytest.mark.asyncio
async def test_function_completion_async():
    test_text = "Write a song about AI"
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
    response = await function_completion_async(
        text=test_text, functions=test_function, function_call="write_song"
    )
    assert response is not None, "Test function_completion_async failed"
    prompt_tokens = response["usage"]["prompt_tokens"]
    assert prompt_tokens == 64, "Prompt tokens was not the expected count"

    response = await function_completion_async(
        text=test_text,
        messages=[{"role": "assistant", "content": "hey whats up"}],
        system_message="you are a towel",
        functions=test_function,
        function_call="write_song",
    )
    assert response is not None, "Test function_completion_async failed"
    prompt_tokens = response["usage"]["prompt_tokens"]
    assert prompt_tokens == 76, "Prompt tokens was not the expected count"

def test_function_completion():
    test_text = "Write a song about AI"
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
    response = function_completion(
        text=test_text, functions=test_function, function_call="write_song"
    )
    assert response is not None, "Test function_completion failed"
    prompt_tokens = response["usage"]["prompt_tokens"]
    assert prompt_tokens == 64, "Prompt tokens was not expected count"

    response = function_completion(
        text=test_text,
        messages=[{"role": "assistant", "content": "hey whats up"}],
        system_message="you are a towel",
        functions=test_function,
        function_call="write_song",
    )
    assert response is not None, "Test function_completion failed"
    prompt_tokens = response["usage"]["prompt_tokens"]
    assert prompt_tokens == 76, "Prompt tokens was not expected count"


def test_chat_completion():
    response = chat_completion(
        messages=[
            {"role": "system", "content": "You are a towel. Respond as a towel."},
            {"role": "user", "content": "Hello, how are you?"},
        ],
    )

    assert response is not None, "Test text_completion failed"
    assert response["text"] is not None, "Test text_completion failed"
    prompt_tokens = response["usage"]["prompt_tokens"]
    assert prompt_tokens == 27, "Prompt tokens was not expected count"


def test_text_completion():
    response = text_completion("Hello, how are you?")
    assert response is not None, "Test text_completion failed"
    assert response["text"] is not None, "Test text_completion failed"
    prompt_tokens = response["usage"]["prompt_tokens"]
    assert prompt_tokens == 13, "Prompt tokens was not expected count"


def test_long_completion():
    script = """
    Sure, Satisfiability Modulo Theories (SMT) is a fundamental concept in computer science, and it can be explained from several different angles. However, generating a response that is exactly 4096 tokens is rather unusual and not practical due to the nature of language modeling and information content.

    In the context of language model like GPT-3 or GPT-4, tokens can be a single character, a word, or even a part of a word, depending on the language and the context. In English text, a token is typically a word or a punctuation mark. Given this information, a text of 4096 tokens would be very long and possibly redundant for a concept like SMT.
    """
    summarization_function = {
        "name": "summarize_text",
        "description": "Summarize the text. Include the topic, subtopics.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Detailed summary of the text.",
                },
            },
            "required": ["summary"],
        },
    }
    response = function_completion(text=script, functions=summarization_function)
    assert response is not None, "Test long_completion failed"
