import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

TEXT_MODEL = os.getenv("EASYCOMPLETION_TEXT_MODEL")
if TEXT_MODEL == None or TEXT_MODEL == "":
    TEXT_MODEL = "gpt-3.5-turbo-0613"
LONG_TEXT_MODEL = os.getenv("EASYCOMPLETION_LONG_TEXT_MODEL")
if LONG_TEXT_MODEL == None or LONG_TEXT_MODEL == "":
    LONG_TEXT_MODEL = "gpt-3.5-turbo-16k"

EASYCOMPLETION_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("EASYCOMPLETION_API_KEY")

EASYCOMPLETION_API_ENDPOINT = os.getenv("EASYCOMPLETION_API_ENDPOINT") or "https://api.openai.com/v1"

DEBUG = os.environ.get("EASYCOMPLETION_DEBUG") == "true" or os.environ.get("EASYCOMPLETION_DEBUG") == "True"

DEFAULT_CHUNK_LENGTH = 4096 * 3 / 4  # 3/4ths of the context window size
