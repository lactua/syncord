from os import listdir, remove
for file in listdir("./tmp"): remove("./tmp/"+file)

from src.mods.upstream import upload, download

res = upload('a.jpg', 'abc')
ids = res['ids']
compressed = res['compressed']
download(ids, 'b.jpg', 'abc', compressed)