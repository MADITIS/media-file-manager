from abc import ABC, abstractmethod
from typing import Union, Optional

from pyparsing import Optional

from sorter import logging
from sorter.utils import file_handler, str_handler
from sorter.utils.exceptions.config_err import EnglishTitleMissing

from ..api_utils import Anilist, Anime, AnimeSearch

logger = logging.getLogger(__name__)

class Api(ABC):
    '''
    Abstract Base Class for all the api handling.
    '''
    @abstractmethod
    def search_item(self) -> None:
        ...


class AnilistSearch(Api):
    '''
    Concrete Class implementation for Anilist Api
    '''
    def __init__(self) -> None:
        self.anilist_api = Anilist()

    def search_item(self, title):
        try:
            results = self.anilist_api.get_anime(anime_name=title)
        except IndexError as err:
            logger.error(f'{err!s}')
        else:
            logger.info(results)

class MalApi(Api):
    '''
    Concrete Class implementation for MAL Api
    '''

    def search_item(self, title: str) -> Union[str, None]:
        try:
            search = AnimeSearch(title)
        except ValueError as err:
            logging.warning(f'{err!s} for {title}: Found Nothing on MAL ') 
        else:
            mal_id: int = search.results[0].mal_id
            logging.info(f'Now searching using id: {mal_id} for {search.results[0].title}') 
            return self.search_by_id(mal_id) 

    
    def search_by_id(self, mal_id: int) -> Union[str, None]:
        try:
            response = Anime(mal_id)
        except ValueError as err:
            logging.error(f'No search Results Using MAL ID') 
        else:
            try:
                title: str = response.title_english

                if not title:
                    raise EnglishTitleMissing(f'English Title Not available for {response.title}')
            except EnglishTitleMissing as err:
                logger.warning(f'{err!s}')
                title: str = response.title   
           
            release_date: Union[str, None] = str_handler.get_release_date(response.aired)
            
            if release_date:
                show_folder: str = f'{title} ({release_date})'
            else:
                logger.info(f'Release Date not found for {title}')
                show_folder: str = title


            return show_folder

