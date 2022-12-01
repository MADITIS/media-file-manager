import logging
import os
import random
from typing import Any, List, Union

import sorter
from sorter.settings import config

from ..exceptions.config_err import EmptyFolderError
from ..gdrive import Credentials, HttpError, build, service_account

logger = logging.getLogger(__name__)

class GoogleDrive:
    '''
    Base Class for all Drive Sub classes
    '''
    SERVICE_ACCOUNTS: int = random.randrange(sorter.service_account_index)
    build_object = Any


    def __init__(self) -> None:
        self.__auth_scopes = ['https://www.googleapis.com/auth/drive']
        logger.debug(f"Base Class {__class__.__name__} Initialized.")
        logger.info('Creating Service...')
        self.__service = self.__create_service()
        logger.info(f'Service is created')

        
    def __create_service(self) -> build_object:
        '''
        Main Method To Create Service.
        '''
        logger.info(f'Authorizing with {AnimeGoogleDrive.SERVICE_ACCOUNTS}.json service account') 
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
        except HttpError as err:
            logger.error(f'{err!s} Exiting...')
            exit(0)
        else:
            # add normal account
            ...

        return service


    def is_folder_exist(self, folder_name: str, destination_folder_id: str):   
        query = "name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{destination_folder_id}'\
         in parents and trashed=false"

        token = None
        while True:
            results = self.__service.files().list(
                                    driveId=config.DRIVE_SOURCE_DRIVE_ID,
                                    q=query,
                                    corpora='teamDrive',
                                    supportsAllDrives = True,
                                    pageToken = token,
                                    pageSize = 500,
                                    includeItemsFromAllDrives  = True,	
                                    fields='nextPageToken, files(id,name,mimeType)'
                                    ).execute()

            files = results.get("files", [])
            
            if not files:
                return False
            
            print(files)
            

            token = results.get("nextPageToken")


    # @staticmethod
    # def create_folder(metadata):
    #     create = service.files().create(
    #         supportsAllDrives = True,
    #         body = metadata,
    #         fields = "id",
    #     ).execute()

    #     return create.get("id")    

    # @staticmethod    
    # def move_file(previous_parent,new_parent,file_id,folder_name):
    #     try:
    #         move = service.files().update(
    #             supportsAllDrives = True,
    #             fileId = file_id,
    #             addParents= new_parent,
    #             removeParents = previous_parent,
    #             fields='id, parents, name, size',
    #                     ).execute() 

    #         moved_folder_id = move.get("parents")[0]
    #         name = move.get("name")
    #         size = int(move.get("size"))
    #         fileid = move.get("id")
    #         info_side = info.GetInfo()
    #         move_size = info_side.get_size(size)
    #         info_side.sendinfo(folder_name,name,moved_folder_id,move_size)

    #     except HttpError as err:
    #         pass          


class AnimeGoogleDrive(GoogleDrive): 
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
    



    def __init__(self) -> None:
        '''
        Parameters:
        -----------
        __auth_scopes: List[str]
                    Required Permissions to Build the serivice.

        __services: Service Object
                Builds the service for the Api        
        '''
        super().__init__()

        self.__initial_search_results: list[dict[str, str]] = []
    

    def __str__(self) -> str:
        return f'{__class__.__name__} ({self})'


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
            results = self._GoogleDrive__service.files().list( #type: ignore
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

        logger.debug('Search Finished\n_____________________________________________________________________________________\
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
