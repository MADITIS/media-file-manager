import logging
import os
import random
from typing import Any, List, Union
import guessit

import sorter
from sorter.settings import config

from sorter.utils.exceptions.config_err import EmptyFolderError
from sorter.utils.gdrive import Credentials, HttpError, build, service_account

logger = logging.getLogger(__name__)

class GoogleDrive:
    '''
    Base Class for all Drive Sub classes
    '''
    SERVICE_ACCOUNTS: int = random.randrange(sorter.service_account_index)
    build_object = Any
    drive_files = list[dict[str, str]]


    def __init__(self) -> None:
        self.__auth_scopes = ['https://www.googleapis.com/auth/drive']
        logger.info(f"Base Class {__class__.__name__} Initialized.")
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


    def list_method(self, query: str, token: Union[str, None]=None, drive_id: str=config.DRIVE_DESTINATION_DRIVE_ID) -> build_object:
        results = self.__service.files().list(
                                    driveId=drive_id,
                                    q=query,
                                    corpora='teamDrive',
                                    supportsAllDrives = True,
                                    pageToken = token,
                                    pageSize = 500,
                                    includeItemsFromAllDrives  = True,	
                                    fields='nextPageToken, files(id,name,mimeType)'
                                    ).execute()
        return results


    def __unpack_folder(self, folder_id: str, mimetype: str) -> Union[drive_files, None]:
        query = f"'{folder_id}' in parents and mimeType='{mimetype}' and trashed = false"
        result_files: GoogleDrive.drive_files = []

        token = None
        while True:
            results = self.list_method(query=query, token=token)

            files = results.get("files", [])
            result_files += files
            token = results.get('nextPageToken', None)

            if not token:
                result = result_files if result_files else None
                return result



    def __is_folder_exist(self, folder_name: str, check_folder_id: str=config.DRIVE_DESTINATION_FOLDER_ID, mimetype: str='application/vnd.google-apps.folder'):   
        query = f"name='{folder_name}' and mimeType='{mimetype}' and '{check_folder_id}' in parents and trashed=false"

        while True:
            results = self.list_method(query=query)

            files = results.get("files", [])
            
            if not files:
                return False
    
            logger.info(f'{folder_name} already exists: Results Found {files}')
            return files


    def __create_folder(self, folder_name: str, parents: str=config.DRIVE_DESTINATION_FOLDER_ID) -> str:
        metadata = {
            'name': folder_name,
            'parents': [parents],
            'mimeType': 'application/vnd.google-apps.folder' 
        }

        create = self.__service.files().create(
            supportsAllDrives = True,
            body = metadata,
            fields = "id",
        ).execute()

        return create.get("id")    


    def prepare_folders(self, folder_name: str, file_name: dict[str, str]) -> Union[str, None]:
        kwargs = {
            'old_parent': ','.join(file_name['parents']),
            'release_name': file_name['name'],
            'folder_id': file_name['id'],
            'mimetype': file_name['mimeType']
        }

        is_folder_exist = self.__is_folder_exist(folder_name)
        
        if is_folder_exist:
            new_parent = is_folder_exist[0]['id']
            kwargs['new_parent'] = new_parent
            self.move_after_check(kwargs=kwargs)
        else:
            new_parent = self.__create_folder(folder_name)
            kwargs['new_parent'] = new_parent
            self.move_after_check(kwargs=kwargs)

                    
    def move_after_check(self,**kwargs):
        print(kwargs)
        
        if kwargs['kwargs']['mimetype'] == 'application/vnd.google-apps.folder':

                is_folder_exist = self.__is_folder_exist(folder_name=kwargs['kwargs']['release_name'], check_folder_id=kwargs['kwargs']['new_parent'])

                if is_folder_exist:
                    logger.warning(f"{kwargs['kwargs']['release_name']} Already Exists.")
                    # here work
                    return
                else:
                    new_parent = self.__create_folder(kwargs['kwargs']['release_name'], parents=kwargs['kwargs']['new_parent'])
                    is_movable = self.__unpack_folder(kwargs['kwargs']['folder_id'], kwargs['kwargs']['mimetype'])

                    if is_movable:
                        for move_file in is_movable:
                            self.__move(old_parent=kwargs['kwargs']['old_parent'], new_parent=new_parent, file_to_move=move_file['id'])
                    else:
                        logger.warning(f"{kwargs['kwargs']['release_name']} is a empty Folder.")


        elif kwargs['kwargs']['mimetype'] == 'video/x-matroska' or kwargs['kwargs']['mimetype'] == "video/mp4":
            result = guessit.guessit(kwargs['kwargs']['release_name'])
            new_release_name = f'[{result["release_group"]}] {result["title"]} ({result["source"]} {result["screen_size"]} {result["video_profile"]} {result["audio_codec"]})'
            is_folder_exist = self.__is_folder_exist(new_release_name, kwargs['kwargs']['new_parent'], kwargs['kwargs']['mimetype'])

            if is_folder_exist:
                logger.warning(f'{new_release_name} File Already exists.')
                new_parent = is_folder_exist[0]['id'] 
            else:
                new_parent = self.__create_folder(new_release_name)

            self.__move(old_parent=kwargs['kwargs']['old_parent'], new_parent=new_parent, file_to_move=kwargs['kwargs']['folder_id'])


   
    def __move(self, old_parent: str, new_parent: str, file_to_move: str):

        try:
            move = self.__service.files().update(
                supportsAllDrives = True,
                fileId = file_to_move,
                addParents= new_parent,
                removeParents = old_parent,
                fields='id, parents, name, size',
                        ).execute() 
            # moved_folder_id = move.get("parents")[0]
            # name = move.get("name")
            # size = int(move.get("size"))
            # fileid = move.get("id")
            # info_side = info.GetInfo()
            # move_size = info_side.get_size(size)
            # info_side.sendinfo(folder_name,name,moved_folder_id,move_size)

        except HttpError as err:
            logger.error(f'unexpected Error ocured while moving: {err!s}')      
        else:
            name = move.get("name")
            logger.info(f'Moved Successfully {name}')


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
        logger.info('Starts Searching\n_____________________________________________________________________________________\
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

        logger.info('Search Finished\n_____________________________________________________________________________________\
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
