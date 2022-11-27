from sorter import logging
from pathlib import Path
import os
from typing import Callable, Type, List, Union
import csv

logger = logging.getLogger(__name__)

class ModifyName:
    '''
    Handles any string related cases.
    '''
    def __init__(self) -> None:
        self.exclude = ['v1', 'v2', 'v3', 'OVA', 'Season', 'COMPLETE', '2nd', 'Seasons', '001-', 'S1', 'S2', "- 0"]


    def is_best_release(self, name: str, best_release: List[str]) -> bool:
        return True if name in best_release else False


    def cleaned(self, title: str) -> Union[str, None]:
        for i in self.exclude:
            if i in title:
                try:
                    title = title.split(i)[0].strip()
                except (IndexError, AttributeError) as err:
                    logger.error(f'{err!s}')
                    continue 
                else:
                    return title
        return title
    
    # def test2(cls)

    @staticmethod
    def test():
        ...
    

class File:
    def __init__(self) -> None:
        self.best_release_names: List[str] = self.get_best_release()
        self.english_names = self.get_english_names()
        self.alt_names = self.get_alt_names()

    
    def get_best_release(self) -> List[str]:
        file_path =os.path.abspath('sorter\\internal_files\\names.csv')

        try:
            release_file = open(file=file_path, encoding='utf-8')

        except IOError as err:
            logger.error(f'{err!s}')
            exit(0)
        else:
            with release_file:
                lines = csv.DictReader(release_file)
                result = [line['name'] for line in lines]
            return result

    def get_english_names(self):
        ...

    def get_alt_names(self):
        ...

