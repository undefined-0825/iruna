import glob
from lib import write_text

contents = ''
files = glob.glob("./*.py")

for file in files:
    contents += '------------------------------------\n'
    contents += file + '\n'
    contents += '------------------------------------\n'

    with open(file, mode='r', encoding = 'utf-8') as f:
        contents += f.read()
        contents += '\n\n\n\n'


    write_text('./pack.txt', contents)
