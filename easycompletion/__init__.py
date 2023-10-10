from .model import (
    function_completion,
    function_completion_async,
    text_completion,
    text_completion_async,
    chat_completion,
    chat_completion_async,
    build_model_info,
)

openai_function_call = function_completion
openai_text_call = text_completion

from .prompt import (
    compose_prompt,
    trim_prompt,
    chunk_prompt,
    count_tokens,
    compose_function,
    get_tokens,
)

from .constants import (
    TEXT_MODEL,
    LONG_TEXT_MODEL,
    DEFAULT_CHUNK_LENGTH,
)

__all__ = [
    "function_completion",
    "text_completion",
    "chat_completion",
    "function_completion_async",
    "text_completion_async",
    "chat_completion_async",
    "openai_function_call",
    "openai_text_call",
    "compose_prompt",
    "compose_function",
    "trim_prompt",
    "chunk_prompt",
    "count_tokens",
    "get_tokens",
    "build_model_info",
    "TEXT_MODEL",
    "LONG_TEXT_MODEL",
    "DEFAULT_CHUNK_LENGTH",
]
