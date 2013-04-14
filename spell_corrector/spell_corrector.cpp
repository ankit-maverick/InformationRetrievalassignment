#include <stdio.h>
#include <unistd.h>
#include <sys/uio.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <iostream>
#include <string>
#include <string.h>
#include "spellcorrector.h"
using namespace std;

#define LEN 1024
char buffer[LEN];
char qlen[8];
char data[128];
struct sockaddr_in serv_addr, cli_addr;
SpellCorrector corrector;

int server_socket(int portno) {
	int sockfd;

	/* First call to socket() function */
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0) {
		perror("ERROR opening socket");
		exit(1);
	}

	/* Initialize socket structure */
	bzero((char *) &serv_addr, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = INADDR_ANY;
	serv_addr.sin_port = htons(portno);

	/* Now bind the host address using bind() call.*/
	if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
		perror("ERROR on binding");
		exit(1);
	}

	return sockfd;
}

int recieve_call(int sockfd) {
	/* Now start listening for the clients, here process will
	* go in sleep mode and will wait for the incoming connection
	*/
	int client, clilen;
	listen(sockfd,5);
	clilen = sizeof(cli_addr);

	/* Accept actual connection from the client */
	client = accept(sockfd, (struct sockaddr *)&cli_addr, (socklen_t*) &clilen);
	if (client < 0) {
		perror("ERROR on accept");
		exit(1);
	}

	return client;
}

void process_call(int client) {
	/* If connection is established then start communicating */
	int n, len;
	bzero(buffer,256);
	n = read(client, buffer, LEN-1);
	if (n < 0) {
		perror("ERROR reading from socket");
		exit(1);
	}

	//printf("Here is the message: %s\n",buffer);
	int i=5, j=0;
	if(buffer[i] < '0' || buffer[i] > '9') {
		close(client);
		return;
	}

	while(buffer[i] != '/') {
		qlen[j++] = buffer[i++];
	}

	qlen[j] = '\0';
	len = atoi(qlen);
	cout << "Len: " << len << endl;
	i++;
	string query = "";
	for(j=0; j<len; j++) {
		query += buffer[i++];
	}

	string ans;
	if(len == 0) {
		ans = "";
	} else {
		ans = corrector.correct(query);
	}
	
	string dataStr = "{ \"word\": \"" + query + "\", \"status\": ";
	if(query == ans) {
		dataStr += "\"false\" }";
	} else {
		dataStr += "\"true\", \"suggestion\":\"" +  ans + "\" }";
	}

	int datalen = dataStr.length();
	char datastr[32];
	sprintf(datastr, "%d", datalen);
	string datastring(datastr);
	string response = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nConnection: Close\r\nContent-Type: text/html\r\nContent-Length: ";
	response += datastring + "\r\n\r\n" + dataStr;
	//cout << "Request: " << buffer << endl;
	//cout << "Response: " << response << endl;
	cout << "*** Spell Correction Service ***" << endl;
	cout << "Len: " << len << endl;
	cout << "Query: " << query << endl;
	cout << "Correct: " << ans << endl << endl << endl;
	/* Write a response to the client */
	n = write(client, response.c_str(), response.length());
	if (n < 0) {
		perror("ERROR writing to socket");
		exit(1);
	}
	close(client);
}

int main( int argc, char *argv[] ) {
	int server, client, port;
	//cout << "Enter port number: ";
	//cin >> port;
	port = atoi(argv[1]);
	cout << "Loading file . . " << endl;
	corrector.load("data_files/big.txt");
	cout << "Starting Spell Correction Service on port: " << port << endl;
	server = server_socket(port);
	cout << "Spell Correction service started on port# "<< port << " :) . . . . Enjoy!";
	while(true) {
		client = recieve_call(server);
		process_call(client);
	}
	
return 0; 
}