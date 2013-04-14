"""
Execute in the following order --
1. uni.py  ==  Store Unigram model of tokens in desc. order of freq. in test.txt
2. bi.py   ==  Store Bigram model of tokens in desc. order of freq. in test.txt
3. tri.py  ==  Store Triigram model of tokens in desc. order of freq. in test.txt
4. tst.py  == Autocompleting queries

"""

import time
import json
import operator

trigram = {}
chars = ['a','b','c','d','e','f','g','h','i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

start = time.time()
files = ['SentiWordNet.txt', 'big.txt']

def strip_query(query):
    ans = ''
    last = ''
    for c in query:
        if c in chars:
            ans += c
            last = c
        elif last != ' ':
            ans += ' '
            last = ' '
    return ans

for fil in files:
    f = open(fil)
    line = f.readline()

    while(line):
        words = strip_query(line.lower()).split(" ")
        for i in range(len(words) - 2):
            if (words[i] + ' ' + words[i+1]) in trigram:
                if words[i+2] in trigram[words[i] + ' ' + words[i+1]]:
                    trigram[words[i] + ' ' + words[i+1]][words[i+2]] += 1
                else:
                    trigram[words[i] + ' ' + words[i+1]][words[i+2]] = 1
    	    else:
    		    trigram[words[i] + ' ' + words[i+1]] = {}
    		    trigram[words[i] + ' ' + words[i+1]][words[i+2]] = 1
        line = f.readline()

    end = time.time()
    print end - start
    print "Tri length " , len(trigram)


m = open('test.txt','a')


for i in trigram:
    list_dec = sorted(trigram[i].iteritems(), key=operator.itemgetter(1), reverse = True)
    trigram[i] = list_dec

for i in trigram:
    for j in range(len(trigram[i])):
        if trigram[i][j][1] > 6:
            m.write(i + ' ' + trigram[i][j][0] + '\n')
m.close()


