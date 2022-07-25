from telethon import TelegramClient, events, sync
import configparser
from sqlHelper import *
from shorthands import *


class ModerationBot:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        api_id = config['Moderation']['api_id']
        api_hash = config['Moderation']['api_hash']
        bot_token = config['Moderation']['bot_token']

        self.ModerationDB = sqlHelper('moderators.db', 'moderators')

        client = TelegramClient('session_name', api_id, api_hash)
        client.start()

        @client.on(events.NewMessage(pattern='/start'))
        async def handler(event):
            await event.respond('Привет!')
            await event.respond('Проверяю твой статус')
            sender = await event.get_sender()
            sender_ID = sender.id
            sender_status = self.checkUserStatus(sender_ID)
            await event.respond(f'Ваш статус ```{statusEncoding[sender_status]}```')

        client.run_until_disconnected()

    def checkUserStatus(self, telegramID):
        # Возвращает статус пользователя. Супер-админ/Админ/Организация/Обычный пользователь
        answer = self.ModerationDB.getUserByTelegramID(telegramID)
        if answer:
            status = answer[ModerationDataBaseStructure['status']]
        else:
            status = 'ou'
        return status

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
