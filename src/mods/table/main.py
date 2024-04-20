from shutil import copy
from ..JSON import JSON
from ..cache import Cache
from ..upstream import upload, download, edit
from ...imconfig import TABLE_INFOS_PATH

table_infos = JSON(TABLE_INFOS_PATH)

class Table:
    def __init__(self, path: str):
        self.path = path

    def fetch(self):
        table_ids = table_infos.get('ids')
        table_compressed = table_infos.get('compressed')
        download(table_ids, self.path, compressed=table_compressed)

    def push(self):
        res = upload(self.path, compressed=table_compressed)
        table_infos.set('ids', res['ids'])
        table_infos.set('compressed', res['compressed'])

    def getFile(self, file_path: str):
        with open(self.path, 'r') as table:
            while (line := table.readline()):
                if line.split()[0] == file_path:
                    file_infos = line[:-1].split()

                    return {
                        'path': file_infos[0],
                        'hash': file_infos[1],
                        'compressed': bool(file_infos[2]),
                        'ids': file_infos[3:]
                    }
                else:
                    continue
    
    def addFile(self, file_path: str, hash: str, compressed: bool, ids: list[str]):
        with open(self.path, 'a') as table:
            table.write(str.join(' ', (file_path, hash, str(int(compressed)), str.join(' ', ids))) + '\n')
    
    def editFile(self, file_path: str, hash: str, compressed: bool, ids: list[str]):
        new_table_file = Cache()

        with open(self.path, 'r') as table, open(new_table_file.path) as new_table:
            while (line := table.readline()):
                if line.split()[0] == file_path:
                    line = str.join(' ', (file_path, hash, str(int(compressed)), str.join(' ', ids))) + '\n'
                
                new_table.write( line)
        
        copy(new_table_file.path, self.path)

        new_table_file.delete()
    
    def deleteFile(self, file_path: str):
        new_table_file = Cache()

        with open(self.path, 'r') as table, open(new_table_file.path) as new_table:
            while (line := table.readline()):
                if line.split()[0] != file_path: new_table.write(line)

        copy(new_table_file.path, self.path)

        new_table_file.delete()

def addToTable(path: str):
    cache_file = Cache()
    table = Table(cache_file.path)
    table.fetch()
    table.add()