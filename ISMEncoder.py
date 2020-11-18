import os

filename = input()
contents = open(filename).read()
contents.encode('utf8')
open(filename, 'w').write(contents)
