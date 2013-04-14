import json
import socket

#cport = input("Enter Port Number for Spell Correction Service: ")
#qport = input("Enter Port Number for Similar Query Search Service: ")
cport = 6000
qport = 6002

def get_query_suggestion(query):
	tokens = query.split(" ")
	ans = ""
	for token in tokens:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect(('localhost', cport))
		client_socket.send("GET /"+str(len(token)) + "/" + token + "\r\n")
		response = client_socket.recv(1024)
		response = response.split("\r\n\r\n")[1]
		response = json.loads(response)
		if response["status"] == "true":
			ans += response["suggestion"] + " "
		else:
			ans += response["word"] + " "
		client_socket.close()
	return ans

def get_results(query):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(('localhost', qport))
	client_socket.send("GET /"+str(len(query)) + "/" + query + "\r\n")
	response = client_socket.recv(2048)
	response = response.split("\r\n\r\n")[1]
	response = json.loads(response)
	client_socket.close()
	return response


n = int(raw_input())
for i in range(n):
	line = raw_input().split("\t")
	corrected = get_query_suggestion(line[1])
	results = get_results(corrected)
	#print "Corrected Query: " + corrected
	print line[0] + "\t" + line[1]
	print str(len(results)-1)
	for i in range(len(results)-1):
		print results[i]
	print "\n"

