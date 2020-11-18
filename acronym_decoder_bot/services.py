import math

import pandas as pd
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.parts import paginate
from telegram_bot_pagination import InlineKeyboardPaginator

from config.config import COLUMN_NAMES, PATH_TO_DB
from models import AcronymExcelDatabase, Match


class TranslateAcronym(StatesGroup):

    """Represents Bot states within /translate_acronym command"""

    waiting_for_acronym = State()
    waiting_for_number_of_choice = State()


class MyPaginator(InlineKeyboardPaginator):

    """Custom Paginator of the inline keyboard"""

    first_page_label = '<<'
    previous_page_label = '<'
    current_page_label = '-{}-'
    next_page_label = '>'
    last_page_label = '>>'


class PaginatedText:

    """Represents text to be paginated"""

    def __init__(self, text: str, limit=4):
        self.text = text
        self.limit = limit

    def set_limit(self, limit: int):

        self.limit = limit

    def paginate_text(self, page=1, delimiter=' ') -> str:

        paginated_text = paginate(
            data=self.text.split(sep=delimiter),
            page=int(page) - 1,
            limit=self.limit)
        return delimiter.join(paginated_text)

    def show_len(self) -> int:
        return len(self.text.split())

    def show_page_count(self) -> int:

        page_count = int(math.ceil(self.show_len() / self.limit))
        return page_count


def load_acronym_excel_database() -> dict:

    """Loads excel db of EMIAS acronyms and returns a dict"""

    emias = AcronymExcelDatabase(pd.read_excel(PATH_TO_DB))
    emias.rename_columns(COLUMN_NAMES)
    emias.set_column_type('reg_number')
    emias.sort_values_by_ascending('reg_number')
    emias.set_index('acronym')
    emias = emias.to_dict()
    return emias


def create_emias_dict_db() -> Match:

    """Creates and returns a Match instance from db dict"""

    emias_dict_db = Match(source=load_acronym_excel_database())
    return emias_dict_db


emias_dict_db = create_emias_dict_db()
