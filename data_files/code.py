
chars = ['a','b','c','d','e','f','g','h','i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

outfiles = ["out-01.txt","out-02.txt","out-03.txt","out-04.txt","out-05.txt","out-06.txt","out-07.txt","out-08][txt","out-09.txt","out-10.txt"]

infiles = ["user-ct-test-collection-01.txt","user-ct-test-collection-02.txt","user-ct-test-collection-03.txt","user-ct-test-collection-04.txt","user-ct-test-collection-05.txt","user-ct-test-collection-06.txt","user-ct-test-collection-07.txt","user-ct-test-collection-08.txt","user-ct-test-collection-09.txt","user-ct-test-collection-10.txt"]

def strip_query(query):
	if query[:7] == "http://":
		query = query[7:]
	if query[:4] == "www.":
		query = query[4:]
	last = query[-4:]
	if last==".com" or last==".org" or last==".edu":
		query = query[:-4]
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

def process_file(iname, oname):
	i = 0
	dic = {}
	fin = open(iname)
	fout = open(oname, 'w')	#Output is Key : Min Rank : Count
	for line in fin:
		if i == 0:
			i += 1
			continue
		else:
			if i%30000 == 0:
				print i
				print "Dictionary Size: " + str(len(dic.keys()))
				for key in dic.keys():
					fout.write(key + "\t" + str(dic[key]) + "\n")
				dic = {}
			i += 1

		tokens = line.strip().split("\t")
		key = tokens[1].strip()
		key = strip_query(key).strip()
		if key == "":
			continue
		if key in dic.keys():
			val = dic[key]
		else:
			val = 0
		val += 1
		dic[key] = val
	fin.close()
	fout.close()


for i in range(10):
	print "Processing File: " + infiles[i]
	process_file(infiles[i], outfiles[i])
	print "Done with: " + outfiles[i]