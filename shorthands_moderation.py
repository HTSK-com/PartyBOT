# Тут хранятся условные обозначения, используемые в программе

statusEncoding = {  # расшифровка статуса пользователя в moderation.db
    'sa': 'Super Admin',
    'a': 'Admin',
    'o': 'Organisation',
    'ou': 'Ordinary User'
}

ModerationDataBaseStructure = {  # очередность колонок в moderation.db
    'id': 0,
    'status': 1,
    'organisation': 2,
    'tgID': 3,
    'step': 4,
    'other': 5
}

permissionsByStatus = {
    'sa': ['/addNewAdmin', '/publishEvent', '/checkEvents'],
    'a': ['/publishEvent', '/checkEvents'],
    'o': ['/publishEvent']
}

programs = {
    'addNewAdmin': 2,  # Команда "addNewAdmin" имеет 2 этапа. 1) Сообщить id 2) Указать уровень доступа
    'publishEvent': 3,  # Команда "publishEvent" имеет 3 этапа. 1) Отправить фото 2) Отправить текст
    # 3) Указать вручную дату
    'checkEvents': 2
}

PATH_PHOTOS = 'partyFiles\photos'
