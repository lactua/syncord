from os import remove, listdir
for file in listdir('.tmp'): remove(f'.tmp/{file}')

from src.mods.init import init
init()
import src.mods.upstream