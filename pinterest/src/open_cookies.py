import os

path = 'cookies'

files = os.listdir(path)
for name in files:
    print(name)
