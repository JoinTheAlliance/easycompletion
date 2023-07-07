# TODO: Write tests

from language import parse_arguments, use_language_model

# TESTS
# Test parse_arguments
test_input = '{"key1": "value1", "key2": 2}'
expected_output = {"key1": "value1", "key2": 2}
assert parse_arguments(test_input) == expected_output, "Test parse_arguments failed"

# Test use_language_model
test_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a song about AI"},
]
test_functions = [
    {
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
]
test_filename = "test_filename"
arguments = use_language_model(
    test_messages, test_functions, {"name": "write_song"}, test_filename
)
print(arguments["lyrics"])
assert isinstance(arguments, dict), "Test use_language_model failed"

print("All tests complete!")
