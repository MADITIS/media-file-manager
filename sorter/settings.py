class Config:
    '''
    Necessary Config settings.
    '''
    TG_USER_ID: str = 'f'
    AUTHORIZED_GROUPS: list[str] = ['test']

    DRIVE_SOURCE_DRIVE_ID: str = '0AIyUCwBELSPnUk9PVA'
    DRIVE_SOURCE_FOLDER_ID: str = '1alZiCB8v8_9cs3Fttx-FS2G8fDe4_3Kv'

    DRIVE_DESTINATION_DRIVE_ID: str = '0AIyUCwBELSPnUk9PVA'
    DRIVE_DESTINATION_FOLDER_ID: str = '1q7WmyErsI3FqxsMsPuNCm6mPzyoMhRjz'

config = Config()