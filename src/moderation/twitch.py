import ollama
from moderation.ollama import ollama_mod

async def twitch_mod(ollama_client: ollama.AsyncClient, model: str, history: list[str], message: str):
    mod_action = await ollama_mod(ollama_client, model, history, message)
    
    print(f"Twitch Mod action: {mod_action}")