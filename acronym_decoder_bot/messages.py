EMOJI_ARROWS_DOWN = '   '.join(['\U00002B07'] * 9)
EMOJI_ARROWS_RIGHT = '  \U000027A1  '

COMMAND_MESSAGES = {
    'start': 'ВПАБ - Вас Приветствует Акроним Бот!\n\
ЕМИАС любит, когда коротко, Акроним Бот - когда понятно.\n\n\
Карта команд \U0001F609 \n\
/start - Начало работы или сброс бота\n\
/translate_acronym - Перевести акроним\n\
/show_all - Вывести список всех акронимов\n',
    'translate_acronym': 'Пожалуйста, введите акроним ниже',
    'show_all': 'Ниже перечислены все акронимы, которые есть в базе бота',
    'cancel': 'Отменить действие, вернуться к меню',
}

STATE_MESSAGES = {
    'waiting_for_number_of_choice': f'Найдено несколько совпадений.\n\
Пожалуйста, выберите цифру нужного совпадения ниже\n\
{EMOJI_ARROWS_DOWN}',
}
