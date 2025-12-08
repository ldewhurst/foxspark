from discord.ext import commands
from moderation.discord import discord_mod
import ollama
import discord
import asyncio

async def run_discord_client(ollama_client: ollama.AsyncClient, model: str, token: str):
    command_prefix = "!"
    
    intents = discord.Intents.default()
    intents.message_content = True # Must also be set in the developer portal
    
    bot = commands.Bot(command_prefix, intents=intents)
    
    @bot.event
    async def on_ready():
        print(f"Discord: Logged in as {bot.user}")
        
    @bot.event
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return # Ignore messages from self
        asyncio.create_task(discord_mod(ollama_client, model, message))
        
    await bot.start(token)