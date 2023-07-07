# TODO: Write tests and verify these tests are good


from actions import (
    add_action,
    use_action,
    get_action_handler,
    remove_action,
    action_handlers,
)


def test_action_handler(arguments):
    input = arguments["input"]
    return input


# Test for add_action
test_action = {
    "test": {
        "function": {
            "name": "test",
            "description": "A test action",
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "Some test input",
                    },
                },
            },
            "required": ["input"],
        },
        "chain_from": [],
        "dont_chain_from": [],
        "handler": test_action_handler,
    },
}
# for each in test_action:
for each in test_action:
    add_action(each, test_action[each])
assert each in action_handlers

# Test for use_action
assert use_action("test", {"input": "test"}) == "test"

# Test for get_action_handler
assert get_action_handler("test") == test_action_handler

# Test for remove_action
remove_action("test")
assert "test" not in action_handlers
