import csv
import os
from pathlib import Path
from typing import Callable, List, Optional, Type, Union

from sorter import logging

logger = logging.getLogger(__name__)

def regex_log(base_func: Callable) -> Callable:
    def wrapper(obj):
        logger.info(f'Executing {base_func.__name__} function')
        base_func(obj)
    
    return wrapper

class ModifyName:
    '''
    Handles any string related cases.
    '''
    def __init__(self) -> None:
        self.exclude = ['v1', 'v2', 'v3', 'OVA', 'Season', 'COMPLETE', '2nd', 'Seasons', '001-', 'S1', 'S2', "- 0"]


    def is_best_release(self, name: str, best_release: List[str]) -> bool:
        return True if name in best_release else False


    def cleaned(self, title: str) -> str:
        for i in self.exclude:
            if i in title:
                try:
                    title = title.split(i)[0].strip()
                except (IndexError, AttributeError) as err:
                    logger.error(f'{err!s}') 
                else:
                    return title
        return title

    def get_release_date(self, air_date: str) -> Union[str, None]:

        try:
            release_date: str = air_date.split(',')[1].split('to')[0].strip()
        except Exception as err:
            logger.error('Some UnexpectedError')
        else:
            return release_date
    
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

    def get_english_names(self, ):
        ...

    def get_alt_names(self):
        ...

file_handler = File()
str_handler = ModifyName()