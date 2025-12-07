from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
from dataclasses import dataclass
from twitchAPI.twitch import Twitch
import ollama
import discord
import logging
import json
import asyncio

# Define a dataclass to hold moderation actions.
@dataclass
class ModAction:
    action: str
    confidence: float
    reason: str

# Get requred environment variable, and raise a ValueError if it's missing.
def getenv_required(key: str) -> str:
    value = getenv(key)
    if value is None:
        raise ValueError(f"{key} not found in environment variables")
    return value

# Function to moderate a message using Ollama.
async def ollama_mod(ollama_client: ollama.AsyncClient, model: str, history: list[str], message: str):
    prompt = f"""
    You are a moderator for a casual online gaming community. 
    - Be reasonable. Do not be overly strict.
    - Only flag messages that cleary break community rules.
    - Take into account recent message history when making your decision.
    
    Recent messages:
    {"\n".join(history)}
    
    New Message:
    {message}
    
    Respond with JSON:
    action: allow | warn | timeout | flag
    confidence: 0-1
    reason: short explanation
    """
    
    messages = [{"role": "user", "content": prompt}]
    response = await ollama_client.chat(model, messages, format="json")
    
    assert(response != None)
    action = json.loads(response.message.content) # type: ignore
    
    return ModAction(
        action=action["action"],
        confidence=action["confidence"],
        reason=action["reason"]
    )
    
# Function to moderate a Discord message.
async def discord_mod(ollama_client: ollama.AsyncClient, model: str, message: discord.Message):
    # Just pulling message history from the API for this version. Caching might be a good idea in future to improve response time.
    history = []
    async for history_message in message.channel.history(limit=10):
        history.append(f"{history_message.author}: {history_message.content}")
        
    mod_action = await ollama_mod(ollama_client, model, history, f"{message.author}: {message.content}")
    
    print(f"Mod action: {mod_action}")

# Run Discord client to moderate the Discord server.
async def run_discord_client(ollama_client: ollama.AsyncClient, model: str):
    command_prefix = "!"
    
    intents = discord.Intents.default()
    intents.message_content = True # Must also be set in the developer portal
    
    token = getenv_required("DISCORD_TOKEN")
    
    bot = commands.Bot(command_prefix, intents=intents)
    
    @bot.event
    async def on_ready():
        print(f"Discord: Logged in as {bot.user}")
        
    @bot.event
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return # Ignore messages from self
        await discord_mod(ollama_client, model, message)
        
    await bot.start(token)
    
# Run Twitch client to moderate Twitch chat.
async def run_twitch_client(ollama_client: ollama.AsyncClient, model: str):
    client_id = getenv_required("TWITCH_CLIENT_ID")
    client_secret = getenv_required("TWITCH_CLIENT_SECRET")
    
    twitch = Twitch(client_id, client_secret)
    await twitch.authenticate_app([])
    
    async def on_ready():
        print("Twitch: Connected to Twitch chat")
        
    print("Twitch: Client is not yet implemented.")

async def main():
    # Setup logging and load environment variables
    logging.basicConfig()
    load_dotenv()
    
    # Initialize Ollama client
    ollama_client = ollama.AsyncClient()
    model = getenv_required("DISCORD_MODEL")
    
    # Check that the model is running
    if model not in map(lambda models: models.model, ollama.list().get("models", [])):
        raise ValueError(f"{model} not found in Ollama models")
    
    # Run Discord and Twitch clients concurrently
    asyncio.create_task(run_discord_client(ollama_client, model))
    asyncio.create_task(run_twitch_client(ollama_client, model))
    await asyncio.Future()
    
asyncio.run(main())
