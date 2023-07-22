import dotenv
from rich.panel import Panel
from rich.console import Console

dotenv.load_dotenv()

console = Console()

DEFAULT_TYPE_COLORS = {
    "unknown": "white",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "prompt": "cyan",
    "success": "green",
    "critical": "red",
    "system": "magenta",
}


def log(
    content,
    type="info",
    color="blue",
    type_colors=DEFAULT_TYPE_COLORS,
    panel=True, # display inside a bordered box panel?
    log=True # should log?
):
    """
    Create an event with provided metadata and saves it to the event log file

    Parameters:
    - content: Content of the event
    - type (optional): Type of the event.
        Defaults to None.
    - type_colors (optional): Dictionary with event types as keys and colors
        Defaults to empty dictionary.
    - panel (optional): Determines if the output should be within a Panel
        Defaults to True.
    - log (optional): Determines if the output should be logged

    Returns: None
    """
    if not log:
        return
    
    color = type_colors.get(type, color)

    if panel:
        console.print(Panel(content, title="easycompletion: " + type, style=color))
    else:
        console.print(content, style=color)
