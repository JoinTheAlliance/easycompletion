from easycompletion.model import parse_arguments
from easycompletion.prompt import (
    compose_prompt,
    trim_prompt,
    chunk_prompt,
    count_tokens,
    get_tokens,
    compose_function,
)


def test_chunk_prompt():
    test_text = "Write a song about AI"
    chunks = chunk_prompt(test_text, chunk_length=2)
    assert len(chunks) == 2, "Test chunk_prompt failed"


def test_trim_prompt_and_get_tokens():
    test_text = "Write a song about AI"
    trimmed = trim_prompt(test_text, max_tokens=2)
    count = count_tokens(trimmed)
    assert count == 2, "Test trim_prompt failed"

    tokens = get_tokens(test_text)
    assert len(tokens) == 5, "Test get_tokens failed"


def test_parse_arguments():
    test_input = '{"key1": "value1", "key2": 2}'
    expected_output = {"key1": "value1", "key2": 2}
    assert parse_arguments(test_input) == expected_output, "Test parse_arguments failed"


def test_compose_prompt():
    test_prompt = "I am a {{object}}"
    test_dict = {"object": "towel"}
    prompt = compose_prompt(test_prompt, test_dict)
    assert prompt == "I am a towel", "Test compose_prompt failed"


def test_compose_function():
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
    composed_summarization_function = compose_function(
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
    assert (
        composed_summarization_function == summarization_function
    ), "Test compose_function failed"
