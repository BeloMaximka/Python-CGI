#!python

import sys
import codecs
 
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("Content-Type: text/html")
print()
print("<h1>Register test</h1>", end='')