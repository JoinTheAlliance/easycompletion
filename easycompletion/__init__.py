"""
easycompletion

Leveraging conversational AI for bicameral decision making.
"""

__version__ = "0.2.0"
__author__ = "Moon (https://github.com/lalalune)"
__credits__ = "https://github.com/lalalune/easycompletion"

from .model import (
    openai_function_call,
    openai_text_call,
    compose_function,
)

from .prompt import (
    compose_prompt,
    trim_prompt,
    chunk_prompt,
    count_tokens,
    get_tokens,
)

from .constants import (
    default_text_model,
    default_chunk_length,
)

__all__ = [
    "openai_function_call",
    "openai_text_call",
    "compose_prompt",
    "compose_function",
    "trim_prompt",
    "chunk_prompt",
    "count_tokens",
    "get_tokens",
    "default_text_model",
    "default_chunk_length",
]
