from cryptography.fernet import Fernet
from os import path, getcwd

FILE_PASS = 'Retrans3eC34O8!'
KEY_FILE = path.join(getcwd(), 'security', 'key_file')


class CrytoException(Exception):
    class KeyFileNotFound:
        pass


class EncryptDecrypt:

    def __init__(self, file_pass=FILE_PASS, key_file=KEY_FILE):
        self.file_pass = file_pass
        self.key_file = key_file
        self.fernet = None

    def generate_new_key(self):
        with open(self.key_file, 'wb') as kf:
            kf.write(Fernet.generate_key())
        kf.close()

    def load_key(self, file=None):
        if file is None and path.isfile(self.key_file):
            with open(self.key_file, 'rb') as kf:
                k = kf.read()
                self.fernet = Fernet(k)
        elif path.isfile(file):
            with open(file, 'rb') as kf:
                k = kf.read()
                self.fernet = Fernet(k)
        else:
            raise CrytoException.KeyFileNotFound


    def encrypt(self, token):
        return self.fernet.encrypt(token)

    def decrypt(self, token):
        return self.fernet.decrypt(token)
