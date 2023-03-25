class Config:
    '''
    Necessary Config settings.
    '''
    TG_USER_ID: str = ''
    AUTHORIZED_GROUPS: list[str] = ['authourized groups']

    DRIVE_SOURCE_DRIVE_ID: str = ''
    DRIVE_SOURCE_FOLDER_ID: str = ''

    DRIVE_DESTINATION_DRIVE_ID: str = ''
    DRIVE_DESTINATION_FOLDER_ID: str = ''

config = Config()
