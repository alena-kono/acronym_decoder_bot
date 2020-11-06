import pandas as pd

from config.config import COLUMN_NAMES, PATH_TO_DB
from models import AcronymExcelDatabase, Match


def load_acronym_excel_database() -> dict:

    """Loads excel db of EMIAS acronyms and returns a dict"""

    emias = AcronymExcelDatabase(
        pd.read_excel(PATH_TO_DB))
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
