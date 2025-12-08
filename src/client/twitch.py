import ollama
from twitchAPI.twitch import Twitch
from twitchAPI.chat import Chat, EventData, ChatMessage
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from moderation.twitch import twitch_mod


async def run_twitch_client(ollama_client: ollama.AsyncClient, model: str, client_id: str, client_secret: str):
    user_scope = [AuthScope.CHAT_READ]
    target_channel = "matrixoverclocker"
    
    twitch = await Twitch(client_id, client_secret)
    auth = UserAuthenticator(twitch, user_scope)
    token, refresh_token = await auth.authenticate() # type: ignore
    await twitch.set_user_authentication(token, user_scope, refresh_token)
    
    message_history = []
    
    async def on_ready(ready_event: EventData):
        await ready_event.chat.join_room(target_channel)
        print("Twitch: Connected to Twitch chat")
        
    async def on_message(message: ChatMessage):
        print(f'in {message.room.name}, {message.user.name} said: {message.text}') # type: ignore
        
        await twitch_mod(ollama_client, model, message_history, f"{message.user.name}: {message.text}")
        
        message_history.append(f"{message.user.name}: {message.text}")
        
    chat = await Chat(twitch)
    
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    
    chat.start()
