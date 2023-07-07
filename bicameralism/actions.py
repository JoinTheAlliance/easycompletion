# TODO: Imported from other project, need to refactor heavily

import json

from agentmemory.memory import create_memory, search_memory

# TODO: Add a way to reload action_handlers without restarting the bot

# Create an empty dictionary to hold the action_handlers
action_handlers = {}

# TODO: Replace this, should be entirely from db
action_history = []

def get_action_history():
    return action_history

def use_action(function_call):
    if function_call is None:
        return {"success": False, "response": "No action"}
    function_name = function_call.get("name")
    args = function_call.get("arguments")
    if function_name is None:
        return {"success": False, "response": "No action name"}
    max_action_retries = 3
    action_retries = 0
    response = None
    while action_retries < max_action_retries:
        action_retries += 1
        response = try_use_action(function_name, args)
        if response["success"] == True:
            return response
        
    if response["success"] == True:
        return response

    if action_retries == max_action_retries:
        return {"success": False, "response": "Action failed to execute after multiple retries."}
        
    
def try_use_action(name, arguments):
    """
    Executes a action based on its name and arguments.

    If the action is present in the 'action_handlers' dictionary, it calls the action with its arguments.
    Also, the usage of a action is logged as an event.
    """

    # if prompts invalid, return False

    # TODO: Store action history in a collection
    # If arguments are a JSON string, parse it to a dictionary
    action_history.append(name)
    # prune action history if it's more than 20
    if len(action_history) > 20:
        action_history.pop(0)
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
            # TODO: validate that the arguments are correct and match the required arguments of the action
        except:
            return {"success": False, "response": "Invalid JSON arguments"}

    # Call the action with its arguments if it exists in the 'action_handlers' dictionary
    if name in action_handlers:
        return {"success": True, "response": action_handlers[name](arguments)}

    return {"success": False, "response": "Action not found"}


def add_action(name, action):
    """
    Adds a new action to the action_handlers dictionary and to the 'action_handlers' collection.

    If the action is not present in the 'action_handlers' collection, it is added.
    """
    # Add the action to the 'action_handlers' dictionary
    action_handlers[name] = action["handler"]
    # If not, add the new action to the 'action_handlers' collection
    create_memory(
        "action",
        text=action['function']['description'],
        metadatas={"name": name, "action_call": json.dumps(action["function"])},
    )


def get_action_handler(name):
    """
    Fetches a action based on its name.

    Returns the action if it is present in the 'action_handlers' dictionary.
    """
    return action_handlers.get(name, None)


def remove_action(name):
    """
    Removes a action based on its name from both the 'action_handlers' dictionary and the 'action_handlers' collection.

    Also, logs the removal of a action as an event.
    """
    if name in action_handlers:
        # Remove the action from the 'action_handlers' dictionary
        del action_handlers[name]
        # TODO: fix me
        collection = memory_client.get_or_create_collection("action")
        # Remove the action from the 'action_handlers' collection
        if collection.get(ids=[name]):
            collection.delete(ids=[name])

def search_action_handlers(arguments):
    return search_memory("action", arguments.get("query"))