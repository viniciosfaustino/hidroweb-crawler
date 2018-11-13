from zipfile import ZipFile

import os
PATH = "/home/vinicios/Downloads"
for file in os.listdir(PATH):
    if file.endswith(".zip"):
        print(os.path.join(PATH, file))
        zip = ZipFile(os.path.join(PATH, file))
        zip.extractall(PATH)
        os.remove(os.path.join(PATH, file))

for file in os.listdir(PATH):
    if file.endswith(".zip"):
        print(os.path.join(PATH, file))
        zip = ZipFile(os.path.join(PATH, file))
        zip.extractall(PATH)
