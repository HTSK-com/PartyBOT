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
    'tgID': 3
}

permissionsByStatus = {
    'sa': ['/addNewAdmin', '/publishEvent', '/checkEvents'],
    'a': ['/publishEvent', '/checkEvents'],
    'o': ['/publishEvent']
}