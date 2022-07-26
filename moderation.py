from telethon import TelegramClient, events, sync
import configparser
from sqlHelper import *
from shorthands_moderation import *


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

            self.changeStep(sender_ID, '')
            self.changeOther(sender_ID, '')

            sender_status = self.checkUserStatus(sender_ID)
            await event.respond(f'Ваш статус ```{statusEncoding[sender_status]}```')
            await event.respond('Вам доступны следующие функции:\n' + "\n".join(permissionsByStatus[sender_status]))

        # Функция публикации нового события
        @client.on(events.NewMessage(pattern='/publishEvent'))
        async def publishEvent(event):
            permission = ['sa', 'a', 'o']

            sender = await event.get_sender()
            sender_ID = sender.id
            sender_status = self.checkUserStatus(sender_ID)

            if sender_status not in permission:
                await event.respond('Неподходящий уровень доступа')

            # Добавить изменения step в базе данных, что бы показать, что пользователь перешел
            # на следующий шаг выполнения команды, а именно на отправку фото и текста

        # Функция добавления нового модератора
        @client.on(events.NewMessage(pattern='/addNewAdmin'))
        async def addNewAdmin(event):
            permission = ['sa']

            sender = await event.get_sender()
            sender_ID = sender.id
            sender_status = self.checkUserStatus(sender_ID)

            if sender_status not in permission:
                await event.respond('Неподходящий уровень доступа')
                return

            self.changeStep(sender_ID, 'addNewAdmin 1')
            await event.respond('Введите id пользовотеля')

        @client.on(events.NewMessage())
        async def unrecognisedMessage(event):
            if event.raw_text[0] == '/':
                return

            sender = await event.get_sender()
            sender_ID = sender.id
            step = self.getUserStep(sender_ID)
            if not step:
                await event.respond('Ошибка')
                return

            scenario, step = str(step).split()

            if scenario == 'addNewAdmin':
                if step == '1':
                    newModerTelegramID = event.raw_text
                    self.changeStep(sender_ID, 'addNewAdmin 2')
                    self.changeOther(sender_ID, newModerTelegramID)
                    self.addNewModerator(newModerTelegramID)
                    await event.respond('Выберите уровень доступа')
            elif scenario == 'publishEvent':
                pass
            elif scenario == 'checkEvents':
                pass



        client.run_until_disconnected()

    def checkUserStatus(self, telegramID):
        # Возвращает статус пользователя. Супер-админ/Админ/Организация/Обычный пользователь
        answer = self.ModerationDB.getUserByTelegramID(telegramID)
        if answer:
            status = answer[ModerationDataBaseStructure['status']]
        else:
            status = 'ou'
        return status

    def getUserStep(self, telegramID):
        # Возвращает этап на котором находится пользователь
        answer = self.ModerationDB.getUserByTelegramID(telegramID)
        if answer:
            return answer[ModerationDataBaseStructure['step']]
        return False

    def changeStep(self, telegramID, step):
        self.ModerationDB.editDataBase(telegramID, 'step', f'"{step}"')

    def changeOther(self, telegramID, other):
        self.ModerationDB.editDataBase(telegramID, 'other', f'"{other}"')

    def getEventsForConfirmation(self):
        # Возвращает список событий, предложенныйх пользователями.
        # Эти события надо будет подтвердить или отклонить

        self.uploadNewEvent()  # После подтвержения, событие удаляется из бд, и вновь добавляется уже как новое
        pass

    def uploadNewEvent(self):
        # Добавляет в бд информацию о новой тусовке
        pass

    def addNewModerator(self, telegramID):
        # Дает(или измнеяет) права доступа для пользователя
        self.ModerationDB.newRecord(['telegramID'], [telegramID])

    def delModerator(self, telegramID):
        # Удаляет модератора
        pass


m = ModerationBot()
