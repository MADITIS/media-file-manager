import re
from typing import Callable, List, Type, Union
from abc import ABC, abstractclassmethod
import guessit
# from guessit import guessit
from sorter import logging
from sorter.utils import file_handler, str_handler, regex_log
from sorter.utils.gdrive.gdrive_helper import AnimeGoogleDrive

from sorter.utils.api_utils.api_helper import AnilistSearch, MalApi
# logging.getLogger('guessit').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class Regex(ABC):

    def pattern_matching(self, patterns: list[str], file_name: str) -> Union[str, None]:
            for pattern in patterns:
                matched = re.search(pattern, file_name)
                
                try:
                    logger.info(f'Matched Title: {matched.group(2)}') #type: ignore
                except (IndexError, AttributeError) as err:
                    logger.error(f'{err!s}')
                else:
                    title = matched.group(2) #type: ignore
                    return title

    def guessit_mathing(self, name: str) -> Union[str, None]:
        result = guessit.guessit(name)

        try:
            title = result['title']
        except KeyError as err:
            logger.error(f'{err!s}: Empty/Invalid string passed to the guessit')
        else:
            logger.info('Matching wtih guessit: Successful')
            return title 



    @abstractclassmethod
    def match_by_regex(self) -> None:
        ...


class AnimeRegex(Regex):
    '''

    '''
    def __init__(self, drive_class: Type[AnimeGoogleDrive]) -> None:
        self.drive = drive_class()
        self.drive_results = self.drive.drive_search_results
        self.apicall = self.ApiCalls(self)
        self._patterns: List[str] = [r"\[(.+?)\] ([a-zA-Z0-9- :'_;,&]+)"]

        logger.info(f'{self!s} Created')


    def __str__(self) -> str:
        return f'Anime Regex Object'


    def __repr__(self) -> str:
        return f'{__class__.__name__} (drive_class={self.drive})'


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
                    logger.info('Next Release\n_____________________________________________________________________________________\
_________________________________________________________________________________________________________________________ '
                         )
                    logger.info(f'Best Release: {result}\n Using Patterns to Match.')

                    title = self.pattern_matching(self._patterns, name)
                    title = None

                    if title:
                        title = str_handler.cleaned(title) 
                        logger.info('found Match using Pattern!')
                    else:
                        logger.info('Pattern Matching Failed, Using Gueesit')
                        title = self.guessit_mathing(name)
                        if not title:
                            continue
                    logger.info(f'Final Title: {title}: Searching On MAL\n\n                                         ..............\
..............................................MAL Search Result......................................................')
                    self.apicall.search_api(title, result)

    class ApiCalls:
        def __init__(self, regex_obj: 'AnimeRegex') -> None:
            self.mal = MalApi()
            self.regex = regex_obj


        def search_api(self, title: str, file_name: dict[str, str]) -> None:
            show_folder = self.mal.search_item(title)

            if show_folder:
                logger.info(f'Search Successfull: {show_folder}')
                logger.info(f'Sorting: {show_folder}\n📝 MOVING: {file_name} => {show_folder}')
                self.regex.drive.prepare_folders(show_folder, file_name)
              


        



