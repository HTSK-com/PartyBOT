from telethon import TelegramClient, events, sync


class ModerationBot:
    def __init__(self):
        pass

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