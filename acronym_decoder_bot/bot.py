import os
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.exceptions import MessageNotModified, MessageTextIsEmpty
from loguru import logger

from messages import COMMAND_MESSAGES, STATE_MESSAGES
from services import (MyPaginator, PaginatedText, TranslateAcronym,
                      emias_dict_db)

logger.add(
    sys.stderr,
    format='{time} {level} {message}',
    colorize=True,
    level='INFO'
    )

bot = Bot(token=os.getenv('TELEGRAM_API_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(
    commands=['start'])
async def process_start_command(message: types.message):

    """This handler will be called when user
    sends /start command"""

    await message.reply(
        text=COMMAND_MESSAGES['start'])


@dp.message_handler(
    commands=['translate_acronym'],
    state='*')
async def process_translate_acronym_command(message: types.Message):

    """This handler will be called when user
    sends /translate_acronym command"""

    await message.reply(
        text=COMMAND_MESSAGES['translate_acronym'])
    await TranslateAcronym.waiting_for_acronym.set()


@dp.message_handler(
    state=TranslateAcronym.waiting_for_acronym,
    content_types=types.ContentTypes.TEXT)
async def proceed_acronym_input(message: types.Message, state: FSMContext):

    """This handler will be called when user
    enters acronym"""
    emias_dict_db.reset()

    emias_dict_db.find_matches_for_pattern(pattern=message.text)
    await state.update_data(proceeded_Match=emias_dict_db)

    if emias_dict_db.is_found:
        await message.answer(
            text=emias_dict_db.display_match_results())
        await state.finish()
        return

    if emias_dict_db.is_few_found:

        choice_keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True)
        for match_id in enumerate(sorted(
                list(emias_dict_db.found_matches.keys())), start=1):
            choice_keyboard.add(str(match_id[0]))

        await message.answer(
            text=STATE_MESSAGES['waiting_for_number_of_choice'])
        await message.answer(
            text=emias_dict_db.display_match_results(),
            reply_markup=choice_keyboard)

        await TranslateAcronym.waiting_for_number_of_choice.set()
        return

    else:
        await message.answer(
            text=emias_dict_db.display_match_results())
        return


@dp.message_handler(
    state=TranslateAcronym.waiting_for_number_of_choice,
    content_types=types.ContentTypes.TEXT)
async def proceed_acronym_choice(message: types.Message, state: FSMContext):

    """This handler will be called when user
    chooses acronym from a list by number via keyboard"""

    already_found_matches = await state.get_data()
    already_found_matches = already_found_matches['proceeded_Match']
    try:
        await message.answer(
            text=already_found_matches.choose_match_from_few(
                int(message.text)),
            reply_markup=ReplyKeyboardRemove())

        await state.finish()
        return

    except MessageTextIsEmpty:
        await message.answer(
            text=f'Вы ввели "{message.text}", \
а нужно цифру от 1 до {already_found_matches.display_len_of_found()}')


@dp.message_handler(
    commands=['show_all'])
async def process_show_command(message: types.Message):

    """This handler will be called when user
    send /show_all command"""

    curr_page = 1
    paged_text = PaginatedText(text=emias_dict_db.show_all())

    inline_page_keyboard = MyPaginator(
        page_count=paged_text.show_page_count(),
        current_page=curr_page).markup

    await message.reply(
        text=paged_text.paginate_text(page=curr_page, delimiter='\n'),
        reply_markup=inline_page_keyboard)


@dp.callback_query_handler(lambda callback_query: True)
async def process_callback_button(callback_query: types.CallbackQuery):

    """This handler processes switching buttons on inline keyboard
    within output /show_all command"""

    curr_page = int(callback_query.data)
    paged_text = PaginatedText(text=emias_dict_db.show_all())

    inline_page_keyboard = MyPaginator(
        page_count=paged_text.show_page_count(),
        current_page=curr_page
        ).markup

    await bot.answer_callback_query(
        callback_query_id=callback_query.id)

    try:
        await bot.edit_message_text(
            text=paged_text.paginate_text(page=curr_page, delimiter='\n'),
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=inline_page_keyboard)
    except MessageNotModified:
        pass
    except MessageTextIsEmpty:
        pass


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def process_any(message):

    """This handler processes every other message from user
    that is not bot command and not within Bot states"""

    await process_start_command(message)


if __name__ == '__main__':

    executor.start_polling(
        dispatcher=dp,
        skip_updates=True)
