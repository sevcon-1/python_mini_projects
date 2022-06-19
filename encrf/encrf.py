# import required module
from cryptography.fernet import Fernet
import pyperclip
from time import strftime, gmtime

tstamp = strftime("%Y-%m-%d_%H-%M-%s", gmtime())


def generate_key():
    # key generation
    key = Fernet.generate_key()

    # string the key in a file
    with open(f'filekey.{tstamp}.key', 'wb') as filekey:
        filekey.write(key)


def encryptf(newkey: bool):

    if newkey:
        generate_key()

    # opening the key
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open('nba.csv', 'rb') as file:
        original = file.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open('nba.csv', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decryptf(key: str):
    '''
    with open('filekey.key', 'rb') as keyf:
        key = keyf.readline()
        print(key)
    '''

    # using the key
    fernet = Fernet(key)

    # opening the encrypted file
    with open('nba.csv', 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open('nba.csv', 'wb') as dec_file:
        dec_file.write(decrypted)


if __name__ == "__main__":
    encryptf(True)
    input("Copy key. Press Enter")
    key = pyperclip.paste()
    decryptf(key)
