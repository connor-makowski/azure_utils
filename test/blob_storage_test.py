# Use local env variables for testing purposes
import os, sys
from decouple import RepositoryEnv

wd=os.path.abspath(os.path.dirname(sys.argv[0]))

# Jump out of test directory
wd = os.path.dirname(wd)

env = RepositoryEnv(wd+'/.env').data
try:
    env_az = RepositoryEnv(wd+'/.env_az').data
except:
    env_az = {}


# Start actual test

from azure_utils.blob_storage import AZContainer

az = AZContainer(
    account_url=env_az.get('AZ_STORAGE_ACCOUNT_URL'),
    account_key=env_az.get('AZ_STORAGE_ACCOUNT_KEY'),
    container_name=env_az.get('AZ_STORAGE_CONTAINER_NAME')
)

files = az.list_files(remote_folderpath='/')

az.upload_file(
    remote_filepath='/test.csv',
    local_filepath=f'{wd}/test_data/upload/test.csv',
    overwrite=True
)

az.download_file(
    remote_filepath='/test.csv',
    local_filepath=f'{wd}/test_data/download/test.csv',
    overwrite=True,
    smart_sync=True
)

az.delete_file(
    remote_filepath='/test.csv'
)

az.sync_to_remote(
    remote_folderpath='/',
    local_folderpath=f'{wd}/test_data/upload/',
    overwrite=True,
)

az.sync_to_local(
    remote_folderpath='/',
    local_folderpath=f'{wd}/test_data/download/',
    overwrite=True,
    smart_sync=True,
)

az.delete_folder(
    remote_folderpath='/',
)

az.clear_local_meta(f'{wd}/test_data/')
