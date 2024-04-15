from typing import Union
from json import load, dump
from os.path import exists
from ...imconfig import CONFIG_PATH

class Config:
    def __init__(self, path: str=CONFIG_PATH) -> None:
        self.path = path

        if not exists(path):
            with open(path, 'w') as file:
                file.write('{}')
        
    def _read(self):
        with open(self.path, 'r') as file:
            confs = load(file)

        return confs
    
    def _write(self, confs: dict):
        with open(self.path, 'w') as file:
            dump(confs, file)
        
    def get(self, path:str):
        confs = self._read()
        
        keys = path.split('/')

        try:
            current = confs
            for key in keys:
                current = current[key]
            
            return current
        except (KeyError, TypeError) as error:
            print(error)
            return None
    
    def set(self, path:str, value:Union[int, str, bool]=None):
        confs = self._read()

        keys = path.split('/')
        
        current = confs
        for index, key in enumerate(keys):
            if index == len(keys) - 1:
                current[key] = value
            elif isinstance(current.get(key), dict):
                current = current[key]
            else:
                current[key] = {}
                current = current[key]
        
        self._write(confs)