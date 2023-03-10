"""
Code mainly from 
https://github.com/dropbox/dropbox-sdk-python/blob/master/example/back-up-and-restore/backup-and-restore-example.py

But with modification to work with it from another file
"""

import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError


# My personal token (Replace with own)
TOKEN = ''

# Allows me to use this in another file
# Code I added
class SaveToDropbox:
    '''
    Class used to save to dropbox
    Make using code from another file easier
    '''
    local_file: str = ''
    backup_path:str = ''
    dbx = None

    # Use initializer to create instance and save to dropbox logic at once
    # Some code from link, but with modifications
    def __init__(self, file_path: str, backup_path: str):
        '''
        Saves txt files to dropbox

        param: str file path
        param: str name of file that is save to dropbox
        '''
        self.local_file = file_path
        self.backup_path = backup_path
        if (len(TOKEN) == 0):
            print("No token...")

        # Create an instance of a Dropbox class, which can make requests to the API.
        print("Creating a Dropbox object...")
        with dropbox.Dropbox(TOKEN) as self.dbx:

            # Check that the access token is valid
            try:
                self.dbx.users_get_current_account()
            except AuthError:
                sys.exit("ERROR: Invalid access token; try re-generating an "
                    "access token from the app console on the web.")

            # Create a backup of the current settings file
            self.backup()

            print("Done!")

     # NOTE: all this code is from the link mentioned above.
     # I reused it because there is no need to reinvent the wheel 
     # and it does what I wanted       
    
    # Uploads contents of local_file to Dropbox
    def backup(self):
        with open(self.local_file, 'rb') as f:
            print("Uploading " + self.local_file + " to Dropbox as " + self.backup_path + "...")
            try:
                self.dbx.files_upload(f.read(), self.backup_path, mode=WriteMode('overwrite'))
            except ApiError as err:
                # This checks for the specific error where a user doesn't have
                # enough Dropbox space quota to upload this file
                if (err.error.is_path() and
                        err.error.get_path().reason.is_insufficient_space()):
                    sys.exit("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    print(err.user_message_text)
                    sys.exit()
                else:
                    print(err)
                    sys.exit()