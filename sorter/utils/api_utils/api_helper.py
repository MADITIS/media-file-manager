from ..api_utils import Anilist, AnimeSearch
from sorter import logging

from abc import ABC, abstractmethod

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
    Concrete Class implementation for Anilist Api
    '''

    def search_item(self, title) -> None:
        try:
            search = AnimeSearch(title)
        except ValueError as err:
            logging.error(f'{err!s} for {title}') 
        else:
            logging.info(search.results[0].title) 


def test(query):
    test = AnimeSearch(query)
    print(test.results[0].title)