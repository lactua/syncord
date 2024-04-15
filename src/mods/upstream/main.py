from time import time_ns
from hashlib import sha256
from random import shuffle, seed
from requests import request
from os import remove
from os.path import getsize
from ..config import Config
from ..xor import encrypt, decrypt
from ...imconfig import UPSTREAM_FILE_SIZE, MAX_LOADED_RAM

config = Config()
webhook_url = config.get('webhook/url')

def checkPasskey(passkey: str) -> bool:
    correct_passkey_hash = config.get('vault/passkey_hash')

    if sha256(passkey.encode()).hexdigest() == correct_passkey_hash:
        return True

    return False

def askForPasskey() -> str:
    passkey_hash = config.get('vault/passkey_hash')

    while not checkPasskey(passkey := input('Vault passkey > ')):
        print('Incorrect passkey')
    
    return passkey

def upload(path: str, passkey: str = None) -> list[str]:
    file_name = path.split('/')[-1]
    tmp_path = f'tmp/{file_name}'

    if passkey:
        if not checkPasskey(passkey):
            passkey = askForPasskey()
    else: passkey = askForPasskey()

    print("Encrypting...")

    with open(path, 'rb') as file:
        while (chunk := file.read(MAX_LOADED_RAM)):
            with open(tmp_path, 'ab') as cache_encrypted_file:
                cache_encrypted_file.write(encrypt(passkey, chunk))

    print("Uploading...")

    chunk_size = int(UPSTREAM_FILE_SIZE*10**6*1.048576)

    ids = []

    with open(tmp_path, 'rb') as file:
        while (chunk := file.read(chunk_size)):
            res = request('POST', config.get('webhook/url'), files={'file':('syncord', chunk)})
            ids.append(res.json()['id'])

    remove(tmp_path)
    
    return ids

def download(ids: list[str], path: str, passkey: str = None) -> None:
    


def delete(): pass