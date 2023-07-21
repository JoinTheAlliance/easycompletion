import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

DEFAULT_TEXT_MODEL = os.getenv("OPENAI_MODEL")
if DEFAULT_TEXT_MODEL == None or DEFAULT_TEXT_MODEL == "":
    DEFAULT_TEXT_MODEL = "gpt-3.5-turbo-0613"
LONG_TEXT_MODEL = os.getenv("OPENAI_MODEL_16K")
if LONG_TEXT_MODEL == None or LONG_TEXT_MODEL == "":
    LONG_TEXT_MODEL = "gpt-3.5-turbo-16k"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DEBUG = os.environ.get("DEBUG")

DEFAULT_CHUNK_LENGTH = 4096 * 3 / 4 # 3/4ths of the context window size