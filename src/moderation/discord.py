from moderation.ollama import ollama_mod
import discord
import ollama

# Function to moderate a Discord message.
async def discord_mod(ollama_client: ollama.AsyncClient, model: str, message: discord.Message):
    # Just pulling message history from the API for this version. Caching might be a good idea in future to improve response time.
    history = []
    async for history_message in message.channel.history(limit=10):
        history.append(f"{history_message.author}: {history_message.content}")
        
    mod_action = await ollama_mod(ollama_client, model, history, f"{message.author}: {message.content}")
    
    print(f"Discord Mod action: {mod_action}")