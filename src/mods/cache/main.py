from os import remove
from time import time_ns
from os import mkdir
from os.path import exists
from ...imconfig import CACHE_PATH


class Cache:
    def __init__(self, init_bytes: bytes=b'') -> None:
        if not exists(CACHE_PATH): mkdir(CACHE_PATH)

        self.path = CACHE_PATH + str(time_ns())

        with open(self.path, 'wb') as file:
            file.write(init_bytes)

    def delete(self):
        remove(self.path)