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

unigram = {}
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
        for w in words:
            w = w.lower()
            if w in unigram:
    		    unigram[w] += 1
            else:
                unigram[w] = 1
        line = f.readline()

   
    end = time.time()

    print end - start
    print "Uni length " , len(unigram)

# Sorting the tokens in order of decreasing frequency
# and writing the top 25% of them in test.txt
sorted_uni = sorted(unigram.iteritems(), key=operator.itemgetter(1),reverse=True)

f = open('test.txt','w')
for i in range(len(sorted_uni)/4):
	f.write(sorted_uni[i][0] + '\n')
f.close()



