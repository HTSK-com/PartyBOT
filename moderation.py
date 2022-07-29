from telethon import TelegramClient, events, sync
import configparser

from telethon.tl.functions.users import GetFullUserRequest

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
        self.EventsDB = sqlHelper('events.db', 'events')

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

            self.changeStep(sender_ID, 'publishEvent 1')
            await event.respond('Отправьте картинку афиши')

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
            if event.raw_text != '' and event.raw_text[0] == '/':
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
                    newModerTelegramName = event.raw_text
                    newModerInf = await client(GetFullUserRequest(newModerTelegramName))
                    newModerTelegramID = str(newModerInf.user.id)

                    self.changeStep(sender_ID, 'addNewAdmin 2')
                    self.changeOther(sender_ID, newModerTelegramID)
                    self.addNewModerator(newModerTelegramID)

                    await event.respond('Выберите уровень доступа')
                elif step == '2':
                    newAdminID = self.getUserOther(sender_ID)
                    newAdminStatus = event.raw_text
                    self.changeStatus(newAdminID, newAdminStatus)

                    self.changeStep(sender_ID, '')
                    self.changeOther(sender_ID, '')

                    await event.respond(f'Отлично. Новый админ добавлен\n{newAdminID}\n'
                                        f'{statusEncoding[newAdminStatus]}')

            elif scenario == 'publishEvent':
                if step == '1':  # Фото
                    # Необходимо сделать инструмент для работы с бд events.db
                    path = await client.download_media(event.media, PATH_PHOTOS)
                    filename = path.rstrip('.jpg').lstrip(PATH_PHOTOS)

                    self.uploadNewEvent(filename)
                    self.changeOther(sender_ID, filename)
                    self.changeStep(sender_ID, 'publishEvent 2')

                    await event.respond('Картинка успешно добавлена. Отправьте описание')

                elif step == '2':  # Описание
                    eventDescription = event.raw_text
                    filename = self.getUserOther(sender_ID)

                    file = open(PATH_DESCRIPTIONS + 'desc' + filename, 'wt', encoding='utf-8')
                    file.write(eventDescription)
                    file.close()

                    self.changeStep(sender_ID, 'publishEvent 3')

                    await event.respond('Теперь отправьте дату в формате дд/мм/гггг')

                elif step == '3':  # Дата
                    filename = self.getUserOther(sender_ID)
                    date = event.raw_text
                    self.changeDateInEvent(filename, date)

                    self.changeStep(sender_ID, '')
                    self.changeOther(sender_ID, '')

                    event.respond('Новвя тусовка успешно добавлена')

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

    def getUserOther(self, telegramID):
        # Возвращает этап на котором находится пользователь
        answer = self.ModerationDB.getUserByTelegramID(telegramID)
        if answer:
            return answer[ModerationDataBaseStructure['other']]
        return False

    def changeStatus(self, telegramID, status):
        self.ModerationDB.editDataBase(telegramID, 'status', f'"{status}"')

    def changeStep(self, telegramID, step):
        self.ModerationDB.editDataBase(telegramID, 'step', f'"{step}"')

    def changeOther(self, telegramID, other):
        self.ModerationDB.editDataBase(telegramID, 'other', f'"{other}"')

    def changeDateInEvent(self, filename, date):
        self.EventsDB.editDataBase(f'"{filename}"', 'date', f'"{date}"', 'filename')

    def getEventsForConfirmation(self):
        # Возвращает список событий, предложенныйх пользователями.
        # Эти события надо будет подтвердить или отклонить

        self.uploadNewEvent()  # После подтвержения, событие удаляется из бд, и вновь добавляется уже как новое
        pass

    def uploadNewEvent(self, filename):
        # Добавляет в бд информацию о новой тусовке
        self.EventsDB.newRecord(['filename'], [f'"{filename}"'])

    def addNewModerator(self, telegramID):
        # Дает(или измнеяет) права доступа для пользователя
        self.ModerationDB.newRecord(['telegramID'], [telegramID])

    def delModerator(self, telegramID):
        # Удаляет модератора
        pass


m = ModerationBot()
