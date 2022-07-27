from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
async def get_user(username):
    async with TelegramClient('ваш username', API_ID, API_HASH) as client:
        user = await client(GetFullUserRequest(username))
    return user