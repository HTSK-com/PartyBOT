from telethon import TelegramClient, events, sync
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
api_id = config['Moderation']['api_id']
api_hash = config['Moderation']['api_hash']
bot_token = config['Moderation']['bot_token']

client = TelegramClient('session_name', api_id, api_hash)
client.start(bot_token=bot_token)


@client.on(events.NewMessage(pattern='0'))
async def handler(self, event):
    await event.respond('Hey!')

client.run_until_disconnected()
