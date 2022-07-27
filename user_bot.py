from telethon import TelegramClient, events, sync
import configparser


class MoscowEventsBot:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        api_id = config['User_bot']['api_id']
        api_hash = config['User_bot']['api_hash']
        bot_token = config['User_bot']['bot_token']

        client = TelegramClient('session_name', api_id, api_hash)
        client.start()

        @client.on(events.NewMessage(pattern='/start'))
        async def handler(event):
            await event.respond('Привет!')

        client.run_until_disconnected()


us = MoscowEventsBot()
