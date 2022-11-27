import re
from sorter.utils.gdrive.gdrive_helper import GoogleDrive
from sorter import logging
from typing import Callable, Type, List
from .misc_helper import File, ModifyName
from ..api_utils.api_helper import AnilistSearch, test, MalApi

logger = logging.getLogger(__name__)

def regex_log(base_func: Callable) -> Callable:
    def wrapper(obj):
        logger.info(f'Executing {base_func.__name__} function')
        base_func(obj)
    
    return wrapper

class Regex:
    '''Base Class For all regex operations'''
    ...


class AnimeRegex:
    def __init__(self, drive_class: Type[GoogleDrive]) -> None:
        self.drive_results = drive_class().drive_search_results
        self.release_object = File()
        self.string_obj = ModifyName()
        self._patterns: List[str] = [r"\[(.+?)\] ([a-zA-Z0-9- :'_;,&]+)"]

        logger.info(f'{self!s} Created')


    def __str__(self) -> str:
        return f'Anime Regex Object'


    @regex_log
    def match_by_regex(self) -> None:
        # logger.info(f'Executing {self.match_by_regex.__name__} function')

        for result in self.drive_results:
            try:
                name = result['name']
            except KeyError as err:
                logger.error(f'{err!s}')
            # logger.info(f'Checking {result}...')
            else:
                if self.string_obj.is_best_release(name, self.release_object.best_release_names):
                    logger.debug('Next Release\n_____________________________________________________________________________________\
_________________________________________________________________________________________________________________________ '
                         )
                    logger.info(f'Best Release: {result}')
                    for pattern in self._patterns:
                        matched = re.search(pattern, name)
                        
                        try:
                            logger.info(f'Matched Title: {matched.group(2)}') #type: ignore
                        except (IndexError, AttributeError) as err:
                            logger.error(f'{err!s}')
                            continue
                        else:
                            title = matched.group(2) #type: ignore
                            cleaned_title = self.string_obj.cleaned(title) #type: ignore
                            logger.info(f'Cleaned Title: {cleaned_title}: Searching On MAL\n\n...........................................................\
..............................................MAL Search Result.................................................................................')
                            self.search_api(cleaned_title)
                            break

    
                
                
    def search_api(self, title):
        # Ani_list = AnilistSearch()
        # Ani_list.search_item(title)
#         logger.debug(f'Searching On MAL\n...............................................................................MAL Search Result......................................\
# ..................................'
#                             )
        mal = MalApi()
        mal.search_item(title)



