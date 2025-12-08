from dataclasses import dataclass
import json
import ollama

# Define a dataclass to hold moderation actions.
@dataclass
class ModAction:
    action: str
    confidence: float
    reason: str
    
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