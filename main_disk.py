#!/usr/bin/python

import os

#spell_port = raw_input("Enter Port Number for Spell Correction Service: ")
#auto_port = raw_input("Enter Port Number for Auto Suggestion Service: ")
#search_port = raw_input("Enter Port Number for Similar Query Search Service: ")
spell_port = "6000"
auto_port = "6001"
search_port = "6002"


os.system("g++ spell_corrector/spell_corrector.cpp -o corrector")
os.system("./corrector " + spell_port + " &")

os.system("python auto_complete/tst.py " + auto_port + " &")

os.system("java -jar QuerySearcherDisk.jar " + search_port + "&")
