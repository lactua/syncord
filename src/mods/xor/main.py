from random import seed, randint
from hashlib import sha256

class CryptionKey:
    def __init__(self, key: bytes) -> None:
        self.key = sha256(key).digest()
        seed(self.key)

    def __iter__(self) -> None:
        return self
    
    def __next__(self) -> bytes:
        return randint(1, 255)

def make(key: bytes, file_path: str, dest_path: str) -> None:
    hashed_key = sha256(key).digest()
    cryption_key = CryptionKey(hashed_key)

    with open(file_path, 'rb') as file, open(dest_path, 'wb') as dest:
        while (byte := file.read(1)):
            dest.write(bytes([ord(byte) ^ next(cryption_key)]))