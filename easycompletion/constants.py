import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

TEXT_MODEL = os.getenv("EASYCOMPLETION_TEXT_MODEL") or "gpt-3.5-turbo-0613"
TEXT_MODEL_WINDOW = os.getenv("EASYCOMPLETION_TEXT_MODEL_WINDOW") or 4096
LONG_TEXT_MODEL = os.getenv("EASYCOMPLETION_LONG_TEXT_MODEL") or "gpt-3.5-turbo-16k"
LONG_TEXT_MODEL_WINDOW = os.getenv("EASYCOMPLETION_LONG_TEXT_MODEL_WINDOW") or 16*1024

EASYCOMPLETION_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("EASYCOMPLETION_API_KEY")

EASYCOMPLETION_API_ENDPOINT = os.getenv("EASYCOMPLETION_API_ENDPOINT") or "https://api.openai.com/v1"

DEBUG = (os.environ.get("EASYCOMPLETION_DEBUG") or '').lower() == "true"
SUPPRESS_WARNINGS = (os.environ.get("SUPPRESS_WARNINGS") or '').lower() == "true"

DEFAULT_CHUNK_LENGTH = os.getenv("DEFAULT_CHUNK_LENGTH") or (TEXT_MODEL_WINDOW * 3 // 4)  # 3/4ths of the context window size

DEFAULT_MODEL_INFO = [
    (TEXT_MODEL, DEFAULT_CHUNK_LENGTH),
    (LONG_TEXT_MODEL, LONG_TEXT_MODEL_WINDOW - DEFAULT_CHUNK_LENGTH)
    # In the second case, DEFAULT_CHUNK_LENGTH is used as buffer
]
