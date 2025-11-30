from dotenv import load_dotenv
from os import getenv
import discord
import ollama

load_dotenv()

token = getenv("TOKEN")
if token is None:
    raise ValueError("TOKEN not found in environment variables.")

model = getenv("MODEL")
if model is None:
    raise ValueError("MODEL not found in environment variables.")
if model not in map(lambda m: m.model,  ollama.list().get("models", [])):
    raise ValueError(f"MODEL '{model}' not found in Ollama models.")

async def prompt(input: discord.Message):
    stream = ollama.chat(
        model=model,  # type: ignore - Model guaranteed to be not None here
        messages=[{"role": "user", "content": input.content}],
        stream=True
    )
    buffer = next(stream).message.content
    output = await input.channel.send(buffer)
    for chunk in stream:
        buffer += chunk.message.content
        await output.edit(content=buffer)

# Set up Discord client with intents
intents = discord.Intents.default()
intents.message_content = True # Enable message content intent - Requires enabling in Discord Developer Portal
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

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