"""
Code mainly from https://github.com/dropbox/dropbox-sdk-python/blob/master/example/back-up-and-restore/backup-and-restore-example.py

But with modification to work with if from another file
"""

import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError


# My personal token (Replace with own)
TOKEN = 'sl.BYX4WMpdm4ddGKYOZs4Wpq04Hqs0sCkuTk88AyG7qqrwkJdfV_ZGh8xxhoQaaFVYVdcntaJ6_2eHhKzNrKkLVRzlRNxq196aH0tbjBvUXa8xj4KdbZTHgIio73clqvNtFv7S2Tc'

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
    def __init__(self, file_path: str, backup_path: str):
        '''
        Saves txt files to dropbox

        param: str file path
        param: str name of file that is save to dropbox
        '''
        self.local_file = file_path
        self.backup_path = backup_path
        if (len(TOKEN) == 0):
            sys.exit("ERROR: Looks like you didn't add your access token. "
                "Open up backup-and-restore-example.py in a text editor and "
                "paste in your token in line 14.")

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

            # Restore the local and Dropbox files to a certain revision
            to_rev = self.select_revision()
            self.restore(to_rev)

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

    # Change the text string in local_file to be new_content
    # @param new_content is a string
    def change_local_file(self, new_content):
        print("Changing contents of " + self.local_file + " on local machine...")
        with open(self.local_file, 'wb') as f:
            f.write(new_content)

    # Restore the local and Dropbox files to a certain revision
    def restore(self, rev=None):
        # Restore the file on Dropbox to a certain revision
        print("Restoring " + self.backup_path + " to revision " + rev + " on Dropbox...")
        self.dbx.files_restore(self.backup_path, rev)

        # Download the specific revision of the file at backup_path to local_file
        print("Downloading current " + self.backup_path + " from Dropbox, overwriting " + self.local_file + "...")
        self.dbx.files_download_to_file(self.local_file, self.backup_path, rev)

    # Look at all of the available revisions on Dropbox, and return the oldest one
    def select_revision(self):
        # Get the revisions for a file (and sort by the datetime object, "server_modified")
        print("Finding available revisions on Dropbox...")
        entries = self.dbx.files_list_revisions(self.local_file, limit=30).entries
        revisions = sorted(entries, key=lambda entry: entry.server_modified)

        for revision in revisions:
            print(revision.rev, revision.server_modified)

        # Return the oldest revision (first entry, because revisions was sorted oldest:newest)
        return revisions[0].rev
