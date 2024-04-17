from os.path import getsize
from zlib import compressobj, decompressobj
from ...imconfig import COMPRESSIBILITY_FACTOR_SKIP, COMPRESSIBILITY_FACTOR_TOLERANCE, COMPRESSION_CHUNK_SIZE

def getDifFactor(_set: set):
    _set_mean = sum(_set) / len(_set)
    difs = [((e - _set_mean) / _set_mean)**2 for e in _set]
    difs_mean = sum(difs) / len(difs)
    dif_factor = difs_mean**.5 
    return dif_factor

def getCompressibilityFactor(path):
    bytes_dict = {i: 0 for i in range(256)}
    size = getsize(path)
    
    with open(path, 'rb') as file:
        while (chunk := file.read(int(round(size*COMPRESSIBILITY_FACTOR_SKIP)) + 1)):
            bytes_dict[chunk[0]] += 1

    dif_factor = getDifFactor(set(bytes_dict.values()))
    return dif_factor

def isCompressible(path):
    compressibility_factor = getCompressibilityFactor(path)
    if compressibility_factor >= COMPRESSIBILITY_FACTOR_TOLERANCE:
        return True
    return False

def compressFile(path: str, dest: str):
    compressor = compressobj(memLevel=9)

    with open(path, 'rb') as inputf, open(dest, 'wb') as outputf:
        while (chunk := inputf.read(1024**2)):
            outputf.write(compressor.compress(chunk))
        
        outputf.write(compressor.flush())

def decompressFile(path: str, dest: str):
    decompressor = decompressobj()

    with open(path, 'rb') as inputf, open(dest, 'wb') as outputf:
        while (chunk := inputf.read(1024**2)):
            outputf.write(decompressor.decompress(chunk))
        
        outputf.write(decompressor.flush())