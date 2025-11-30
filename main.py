from dotenv import load_dotenv
from os import getenv
import discord
import ollama

SYSTEM_PROMPT = """
You are a casual, helpful Discord user. Follow these rules:

- Keep responses short and natural.
- Write like a normal human, not an AI.
- Never exceed 10 lines or 1800 characters.
- Avoid markdown except simple inline formatting.
- Never output code unless the user directly requests it.
- No giant paragraphs, no walls of text.
- Never insert more than one blank line at a time.
- Use emojis sparingly and naturally.
"""

# Load environment variables from .env file
load_dotenv()

# Retrieve TOKEN and MODEL from environment variables
token = getenv("TOKEN")
model = getenv("MODEL")
if token is None:
    raise ValueError("TOKEN not found in environment variables.")
if model is None:
    raise ValueError("MODEL not found in environment variables.")
if model not in map(lambda m: m.model,  ollama.list().get("models", [])):
    raise ValueError(f"MODEL '{model}' not found in Ollama models.")

# Function to handle AI prompt and streaming response
async def prompt(message: discord.Message):
    response = None
    async with message.channel.typing():
        response = ollama.chat(
            model=model,  # type: ignore - Model guaranteed to be not None here
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.content},
            ]
        )
    await message.channel.send(response.message.content)

# Set up Discord client with intents
intents = discord.Intents.default()
intents.message_content = True # Enable message content intent - Requires enabling in Discord Developer Portal
client = discord.Client(intents=intents)

# Event handler for when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Event handler for incoming messages
@client.event
async def on_message(message: discord.Message):
    if message.author == client.user: 
        return # Ignore messages from the bot itself
    print(f'Message from {message.author}: {message.content}')
    if message.content.startswith('!ai'):
        await prompt(message)
        return
    
# Run the client with the token from environment variables
client.run(token)