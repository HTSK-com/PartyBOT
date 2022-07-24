from telethon import TelegramClient, events, sync
import configparser


class ModerationBot:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        api_id = config['Moderation']['api_id']
        api_hash = config['Moderation']['api_hash']
        bot_token = config['Moderation']['bot_token']

        client = TelegramClient('session_name', api_id, api_hash)
        client.start(bot_token=bot_token)

        @client.on(events.NewMessage(pattern='0'))
        async def handler(event):
            await event.respond('Hey!')

        client.run_until_disconnected()

    def checkTheUserStatus(self):
        # Возвращает статус пользователя. Супер-админ/Админ/Организация/Обычный пользователь
        pass

    def getEventsForConfirmation(self):
        # Возвращает список событий, предложенныйх пользователями.
        # Эти события надо будет подтвердить или отклонить

        self.uploadNewEvent()  # После подтвержения, событие удаляется из бд, и вновь добавляется уже как новое
        pass

    def uploadNewEvent(self):
        # Добавляет в бд информацию о новой тусовке
        pass

    def addNewModerator(self, telegramID, status):
        # Дает(или измнеяет) права доступа для пользователя
        pass

    def delModerator(self, telegramID):
        # Удаляет модератора
        pass


m = ModerationBot()
