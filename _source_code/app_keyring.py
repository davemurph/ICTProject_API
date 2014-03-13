# keyring backend - code modified from 
# official Keyring documentation, found at
# https://pypi.python.org/pypi/keyring#write-your-own-keyring-backend

from keyring.backend import KeyringBackend

class FlaskAppKeyring(KeyringBackend):
    def __init__(self):
        self.password = ''

    def supported(self):
        return 0

    def get_password(self, service, username):
        return self.password

    def set_password(self, service, username, password):
        self.password = password
        return 0

    def delete_password(self, service, username):
        self.password = None