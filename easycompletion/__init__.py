from .model import (
    function_completion,
    text_completion,
    compose_function,
)

openai_function_call = function_completion
openai_text_call = text_completion

from .prompt import (
    compose_prompt,
    trim_prompt,
    chunk_prompt,
    count_tokens,
    get_tokens,
)

from .constants import (
    DEFAULT_TEXT_MODEL,
    DEFAULT_CHUNK_LENGTH,
)

__all__ = [
    "function_completion",
    "text_completion",
    "openai_function_call",
    "openai_text_completion",
    "compose_prompt",
    "compose_function",
    "trim_prompt",
    "chunk_prompt",
    "count_tokens",
    "get_tokens",
    "DEFAULT_TEXT_MODEL",
    "DEFAULT_CHUNK_LENGTH",
]
