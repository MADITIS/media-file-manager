from ..gdrive import Credentials, build, service_account, HttpError
from ..exceptions.config_err import EmptyFolderError
import sorter
from sorter.settings import config
import logging
import os
import random
from typing import List, Any, Union

logger = logging.getLogger(__name__)

class GoogleDrive:
    '''
    Handles Google Drive Api objects And operations.

    -------------------

    Instance Attributes:
    -------------------
    __auth_scopes: List[str]
                Required Permissions to Build the serivice.

    __services: Service Object
                Builds the service for the Api.
    '''
    
    SERVICE_ACCOUNTS: int = random.randrange(sorter.service_account_index)
    build_object = Any


    def __init__(self) -> None:
        '''
        Parameters:
        -----------
        __auth_scopes: List[str]
                    Required Permissions to Build the serivice.

        __services: Service Object
                Builds the service for the Api        
        '''

        self.__initial_search_results: list[dict[str, str]] = []
        self.__auth_scopes = ['https://www.googleapis.com/auth/drive']
        logger.info('Creating Service...')
        self.__service = self.__create_service()
        logger.info(f'Service is created')
    

    def __str__(self) -> str:
        return f'{__class__.__name__} ({self})'

    
    def __create_service(self) -> build_object:
        '''
        Main Method To Create Service.
        '''
        logger.info(f'Authorizing with {GoogleDrive.SERVICE_ACCOUNTS}.json service account') 
        try:
            cred = service_account.Credentials.from_service_account_file(
                                                        f'accounts/{GoogleDrive.SERVICE_ACCOUNTS}.json',
                                                        scopes=self.__auth_scopes
                                                        )
        except FileNotFoundError as err:
            logger.error(f'{err!s} Exiting...')
            exit(0)


        try:
            service = build('drive', 'v3', credentials=cred)
            logger.info(f'authorization complete with {GoogleDrive.SERVICE_ACCOUNTS}.json service account')
        except (HttpError, FileNotFoundError) as err:
            logger.error(f'{err!s} Exiting...')
            exit(0)
        else:
            pass

        return service

    @property
    def drive_search_results(self) -> list[dict[str, str]]:
        '''
        Lists or searches files in google drive.
        '''
        query = f"'{config.DRIVE_SOURCE_FOLDER_ID}' in parents and trashed = false"
        logger.info(f'Searching {query}')
        logger.debug('Starts Searching\n_____________________________________________________________________________________\
_________________________________________________________________________________________________________________________ '
                         )
        token = None
        while True:
            results = self.__service.files().list(
                                                # q = "parents in '"+self.folder_id+"' and trashed = false",
                                                driveId = config.DRIVE_SOURCE_DRIVE_ID,
                                                q = query,
                                                corpora = 'teamDrive',
                                                supportsAllDrives = True,
                                                pageSize = 500,
                                                pageToken = token,
                                                includeItemsFromAllDrives = True,	
                                                # corpora = 'teamDrive',
                                                fields = 'nextPageToken, files(id,name,mimeType, parents)',
                                                ).execute()
            
            result_files = results.get("files", [])
            logger.info(f'Found: {len(result_files)} results')

            if result_files:
                self.__initial_search_results += result_files

            token = results.get('nextPageToken', None)
            # logger.info(f'token: {token}')
            
            if not token:
                break

        logger.debug('Search Over\n_____________________________________________________________________________________\
_________________________________________________________________________________________________________________________ '
                         )
        logger.info(f'Total Results Found: {len(self.__initial_search_results)}')

        try:
            if not self.__initial_search_results:
                raise EmptyFolderError('Current Search Directory Is Empty')
        except EmptyFolderError as emp:
            logger.error(f'{emp!s} Exiting')
            exit(0)

        return self.__initial_search_results
        # return 'test'


logger.info(f'Imported {__name__}')
