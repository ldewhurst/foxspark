from os import getenv
from dotenv import load_dotenv
from threading import Thread
from client.discord import run_discord_client
from client.twitch import run_twitch_client
import asyncio
import logging
import ollama

# Get requred environment variable, and raise a ValueError if it's missing.
def getenv_required(key: str) -> str:
    value = getenv(key)
    if value is None:
        raise ValueError(f"{key} not found in environment variables")
    return value

def run_client(client_runner, *args):
    asyncio.run(client_runner(*args))
        
# Setup logging and load environment variables
logging.basicConfig()
    
# Load environment variables
load_dotenv()
ollama_model = getenv_required("OLLAMA_MODEL")
discord_token = getenv_required("DISCORD_TOKEN")
twitch_client_id = getenv_required("TWITCH_CLIENT_ID")
twitch_client_secret = getenv_required("TWITCH_CLIENT_SECRET")
    
# Check that the model is running
if ollama_model not in map(lambda models: models.model, ollama.list().get("models", [])):
    raise ValueError(f"{ollama_model} not found in Ollama models")

# Initialize Ollama client
ollama_client = ollama.AsyncClient()
    
# Run clients concurrently
Thread(target=run_client, args=(run_discord_client, ollama_client, ollama_model, discord_token), daemon=True).start()
Thread(target=run_client, args=(run_twitch_client, ollama_client, ollama_model, twitch_client_id, twitch_client_secret), daemon=True).start()

# Keep the main thread alive
while True:
    pass