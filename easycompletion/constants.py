import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

default_text_model = os.getenv("OPENAI_MODEL")
if default_text_model == None or default_text_model == "":
    default_text_model = "gpt-3.5-turbo-0613"
long_text_model = os.getenv("OPENAI_MODEL_16K")
if long_text_model == None or long_text_model == "":
    long_text_model = "gpt-3.5-turbo-16k"

openai_api_key = os.getenv("OPENAI_API_KEY")

default_chunk_length = 4096 * 3 / 4 # 3/4ths of the context window size