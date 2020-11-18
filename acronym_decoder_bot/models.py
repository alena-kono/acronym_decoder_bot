import re

from config.config import MIN_MATCHES_TO_SHOW
from messages import EMOJI_ARROWS_RIGHT


class AcronymExcelDatabase:

    """Represents EMIAS .xlsx database of acronyms as pandas DataFrame"""

    def __init__(self, source):
        self.source = source

    def rename_columns(self, new_column_names: list):
        self.source.columns = new_column_names

    def set_column_type(self, column: str, data_type='str'):
        self.source[column] = self.source[column].astype(data_type)

    def sort_values_by_ascending(self, column: str):
        self.source.sort_values(column, inplace=True)

    def set_index(self, column: str):
        self.source.drop_duplicates(column, keep='last', inplace=True)
        self.source.set_index(column, inplace=True)

    def to_dict(self) -> dict:
        db_dict = self.source.to_dict('index')
        return db_dict


class Match:

    """Represents the pattern matching with the dict"""

    def __init__(self, source: dict):

        self.source = source
        self.found_matches = {}
        self.is_found = False
        self.is_few_found = False
        self.is_too_many_found = False

    def reset(self):

        self.found_matches = {}
        self.is_found = False
        self.is_few_found = False
        self.is_too_many_found = False

    def display_match_results(self):

        if self.is_found:
            for key in self.found_matches.keys():
                return self.found_matches[key]['full_name']

        if self.is_too_many_found:
            return f'Найдено слишком много ({len(self.found_matches)}) \
совпадений.\nПожалуйста, уточните поиск.'

        if self.is_few_found:
            return '\n'.join(
                [str(num) + EMOJI_ARROWS_RIGHT + str(
                    key) for num, key in enumerate(
                    sorted(list(self.found_matches.keys())), start=1)])

        if not self.found_matches:
            return 'Совпадений не найдено.\n\
Пожалуйста, измените Ваш запрос и повторите поиск.'

    def find_matches_for_pattern(self, pattern: str) -> dict:

        for key, value in self.source.items():

            if '"' in pattern or '«' not in pattern:
                lookup_word = re.sub('\\"|\\-|\\«|\\»', '', key)
            else:
                lookup_word = key

            match = re.findall(pattern, lookup_word, flags=re.IGNORECASE)

            if match:
                self.found_matches[key] = value

        def _register_found(self) -> None:
            if not self.found_matches:
                return

            if len(self.found_matches) == 1:
                self.is_found = True

            if len(self.found_matches) <= MIN_MATCHES_TO_SHOW:
                self.is_few_found = True

            if len(self.found_matches) > MIN_MATCHES_TO_SHOW:
                self.is_too_many_found = True

        _register_found(self)

    def choose_match_from_few(self, number_of_choice: int):

        for num, key in enumerate(sorted(
                list(self.found_matches.keys())), start=1):
            if num == number_of_choice:
                return self.found_matches[key]['full_name']

    def display_len_of_found(self):
        return len(self.found_matches)

    def show_all(self):
        return '\n'.join(
            [str(key) + ' -->> ' + str(
                val['full_name']) for key, val in self.source.items()])
