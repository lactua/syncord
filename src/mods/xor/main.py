from random import seed, randint
from hashlib import sha256

def getCryptionKey(key: bytes, length: int) -> bytes:
    hashed_key = sha256(key.encode()).hexdigest().encode()

    seed(sum(hashed_key))

    cryptionKey = bytes(randint(0,255) for _ in range(length))

    return cryptionKey

def encrypt(key: bytes, content: bytes) -> bytes:
    cryption_key = getCryptionKey(key, len(content))

    encrypted_content = bytes([c ^ k for c, k in zip(content, cryption_key)])

    return encrypted_content

def decrypt(key: bytes, encrypted_content: bytes) -> bytes:
    cryption_key = getCryptionKey(key, len(encrypted_content))

    content = bytes([e ^ k for e, k in zip(encrypted_content, cryption_key)])

    return content
