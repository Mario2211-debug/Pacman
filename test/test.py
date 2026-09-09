import os

try:
    with open("/home/mafonso/42 Projects/M4/Pacman/test/test.json") as f:
        data = f.readlines()

    for line in data:
        if line.strip().startswith("#"):
            continue
    print(line)
except Exception as e:
    print(e)
