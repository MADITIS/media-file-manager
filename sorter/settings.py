class Config:
    '''
    Necessary Config settings.
    '''
    TG_USER_ID: str = 'f'
    AUTHORIZED_GROUPS: list[str] = ['test']

    DRIVE_SOURCE_DRIVE_ID: str = '0AOsPUry-ZSICUk9PVA'
    DRIVE_SOURCE_FOLDER_ID: str = '1jcAyD1_XwsGWAyLFBfT2cI6J5buqbghA'

    DRIVE_DESTINATION_DRIVE_ID: str = 'fff'
    DRIVE_DESTINATION_FOLDER_ID: str = 'test'

config = Config()