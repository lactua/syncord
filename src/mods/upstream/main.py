from hashlib import sha384
from requests import request
from ..JSON import JSON
from ..cache import Cache
from ..xor import make
from ..compression import isCompressible, compressFile, decompressFile
from ...imconfig import UPSTREAM_FILE_SIZE, CONFIG_PATH

config = JSON(CONFIG_PATH)
webhook_url = config.get('webhook/url')

def checkPasskey(passkey: str) -> bool:
    correct_passkey_hash = config.get('vault/passkey_hash')

    if sha384(passkey.encode()).hexdigest() == correct_passkey_hash:
        return True

    return False

def askForPasskey() -> str:
    passkey_hash = config.get('vault/passkey_hash')

    while not checkPasskey(passkey := input('Vault passkey > ')):
        print('Incorrect passkey')
    
    return passkey


def upload(path: str, passkey: str = None) -> list[str]:
    cache_file = Cache()

    if passkey:
        if not checkPasskey(passkey):
            passkey = askForPasskey()
    else: passkey = askForPasskey()

    is_compressible = isCompressible(path)

    if is_compressible:
        print("Compressing...")
        compressed_cache_file = Cache()
        compressFile(path, compressed_cache_file.path)
        path = compressed_cache_file.path

    print("Encrypting...")

    make(passkey.encode(), path, cache_file.path)

    print("Uploading...")

    chunk_size = int(UPSTREAM_FILE_SIZE*10**6*1.048576)

    ids = []

    with open(cache_file.path, 'rb') as file:
        while (chunk := file.read(chunk_size)):
            res = request('POST', webhook_url, files={'file':('syncord', chunk)})
            ids.append(res.json()['id'])
    
    cache_file.delete()
    if is_compressible: compressed_cache_file.delete()

    return {'ids': ids, 'compressed': is_compressible}

def download(ids: list[str], path: str, passkey: str = None, compressed: bool=False) -> None:
    cache_file = Cache()

    if passkey:
        if not checkPasskey(passkey):
            passkey = askForPasskey()
    else: passkey = askForPasskey()

    print("Downloading...")

    with open(cache_file.path, 'wb') as file:
        for message in ids:
            res = request('GET', f"{webhook_url}/messages/{message}")
            file_url = res.json()['attachments'][0]['url']
            
            res = request('GET', file_url)
            file.write(res.content)

    if compressed:
        print("Decrypting...")
        decrypted_cache_file = Cache()
        make(passkey.encode(), cache_file.path, decrypted_cache_file.path)
        cache_file.delete()
        cache_file = decrypted_cache_file

        print("Decompressing...")
        decompressFile(cache_file.path, path)
    else:
        print("Decrypting...")
        make(passkey.encode(), cache_file.path, path)

    cache_file.delete()    


def delete(ids: list[str]):
    for message in ids:
        request('DELETE', webhook_url)

def edit(ids: list[str], path: str, passkey: str = None):
    delete(ids)
    upload(path, passkey)