# import required module
from cryptography.fernet import Fernet
import pyperclip
from time import strftime, gmtime

tstamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())


def generate_key():
    # key generation
    key = Fernet.generate_key()

    filekey_name = f'filekey.{tstamp}.key'
    # string the key in a file
    with open(filekey_name, 'wb') as filekey:
        filekey.write(key)

    return filekey_name


def encryptf(filename: str, newkey: bool):

    if newkey:
        filekey_name = generate_key()

    # opening the key
    with open(filekey_name, 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(filename, 'rb') as file:
        original = file.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decryptf(filename: str, key: str):
    '''
    with open('filekey.key', 'rb') as keyf:
        key = keyf.readline()
        print(key)
    '''

    # using the key
    fernet = Fernet(key)

    # opening the encrypted file
    with open(filename, 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open(filename, 'wb') as dec_file:
        dec_file.write(decrypted)


if __name__ == "__main__":
    option = input("Enter e  to encrypt or d to decrypt: ")
    if option == "e":
        filename = input("Enter file inc. path: ")
        encryptf(filename, True)
    elif option == "d":
        filename = input("Enter filename with path to decrypt: ")
        input("Copy key. Press Enter: ")
        key = pyperclip.paste()
        decryptf(filename, key)
