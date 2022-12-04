import logging
from sorter.settings import config
import os
from sorter.utils.exceptions import ServiceAccountMissing, ConfigSettingsMissing


# create a logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,handlers=[logging.FileHandler('sorter/sorter.log', mode='w',
                    encoding='utf-8') ,logging.StreamHandler()], datefmt='%m/%d/%Y %H:%M:%S')

logger = logging.getLogger(__name__)

# check service accounts
service_account_index = len(os.listdir('accounts/'))

try:
    if not service_account_index:
        raise ServiceAccountMissing('Service Accounts are missing. Check accounts folder. Exiting now!')
    elif not (config.AUTHORIZED_GROUPS or config.AUTHORIZED_GROUPS or config.DRIVE_DESTINATION_FOLDER_ID \
            or config.TG_USER_ID or config.DRIVE_SOURCE_FOLDER_ID):

        raise ConfigSettingsMissing('One or More Config Variables are missing. Exiting Now!')
except (ServiceAccountMissing, ConfigSettingsMissing) as err:
    logger.error(f'{err!s}')
    exit(0)
else:
    logger.info(f'Found {service_account_index} Service Accounts.')



logger.info('Started Init!')
