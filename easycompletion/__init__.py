"""
easycompletion

Leveraging conversational AI for bicameral decision making.
"""

__version__ = "0.1.2"
__author__ = "Moon (https://github.com/lalalune)"
__credits__ = "https://github.com/lalalune/easycompletion"

from .language import (
    openai_function_call,
    openai_text_call,
    compose_prompt,
    compose_function,
)

__all__ = [
    "openai_function_call",
    "openai_text_call",
    "compose_prompt",
    "compose_function",
]
