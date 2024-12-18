#!python

import sys
import codecs
 
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("Content-Type: text/html")
print()
with open("home.html", encoding="utf-8") as file:
    print(file.read())