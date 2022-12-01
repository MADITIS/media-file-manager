import re
from typing import Callable, List, Type

from sorter import logging
from sorter.utils import file_handler, str_handler, regex_log
from sorter.utils.gdrive.gdrive_helper import AnimeGoogleDrive

from ..api_utils.api_helper import AnilistSearch, MalApi

logger = logging.getLogger(__name__)

class AnimeRegex:
    '''

    '''
    def __init__(self, drive_class: Type[AnimeGoogleDrive]) -> None:
        self.drive_results = drive_class().drive_search_results
        self.mal = MalApi()
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
                if str_handler.is_best_release(name, file_handler.best_release_names):
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
                        else:
                            title = matched.group(2) #type: ignore
                            cleaned_title = str_handler.cleaned(title) #type: ignore
                            logger.info(f'Cleaned Title: {cleaned_title}: Searching On MAL\n\n                                                 .....................\
..............................................MAL Search Result.............................................................')
                            self.search_api(cleaned_title)
                            break

    
                
                
    def search_api(self, title: str) -> None:
        show_folder = self.mal.search_item(title)

        if show_folder:
            logger.info(f'Search Successfull: {show_folder}')
            logger.info(f'Sorting: {show_folder}: Searching On MAL\n\n                                                 .....................\
..............................................MAL Search Result.............................................................')


        



