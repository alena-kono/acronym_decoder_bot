from pathlib import Path

COLUMN_NAMES = ['full_name', 'acronym', 'reg_number']

PATH_TO_DB = Path.joinpath(
    Path.cwd().parent,
    'db/db_emias.xlsx'
    )

MIN_MATCHES_TO_SHOW = 8

BOT_COMMANDS = [
    {'command': 'start', 'description': 'Начало работы / Сброс бота'},
    {'command': 'translate_acronym', 'description': 'Перевести акроним'},
    {'command': 'show_all', 'description': 'Вывести список всех акронимов'},
]
