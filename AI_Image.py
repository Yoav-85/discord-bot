import os
from dotenv import load_dotenv
from openai_wrapper import OpenAIWrapper

load_dotenv()

# Get the API key from the environment
XAI_API_KEY = os.getenv('XAI_API_KEY')
base_url = "https://api.x.ai/v1"

if not XAI_API_KEY:
    raise ValueError("XAI_API_KEY environment variable is not set.")

client = OpenAIWrapper(api_key=XAI_API_KEY, base_url=base_url, model_name="grok-beta")


def ask_bot(text):
    return client.ask(text)
