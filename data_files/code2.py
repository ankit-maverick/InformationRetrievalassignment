
fout = open("query_set.txt", 'w')	#Output is Key : Min Rank : Count
files = ["out-01.txt","out-02.txt","out-03.txt","out-04.txt","out-05.txt","out-06.txt","out-07.txt","out-08.txt","out-09.txt","out-10.txt"]

def process_file(iname):
	i = 0
	dic = {}
	fin = open(iname)
	
	for line in fin:
		line = line.rstrip()
		if i == 0:
			i += 1
			continue
		else:
			if i%50000 == 0:
				print "\t" + str(i)
				print "\tDictionary Size: " + str(len(dic.keys()))
				for key in dic.keys():
					fout.write(key + "\t" + str(dic[key]) + "\n")
				dic = {}
			i += 1

		tokens = line.split("\t")
		if tokens[0] in dic.keys():
			val = dic[tokens[0]] + int(tokens[1])
		else:
			val = int(tokens[1])
		dic[tokens[0]] = val
	fin.close()

for file in files:
	print "Processing file: " + file
	process_file(file)
fout.close()

