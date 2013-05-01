CS635 Information Retrieval and Web Mining : Assignment

Ankit Agrawal
10D070027

Saif Hasan
09005003

Sagar Chordia
09005013

This assignment submission includes the implementation of various features of a Search Engine after training on 30M query data provided by AOL for research purposes. The implemented features are:

1) Predicting Similar Queries  

2) Query Auto Completion  

3) Spell Checker
**************
Instructions for Running
	- Open one terminal and in it type following command
		$ python main_ram.py
		
		Note: If this gives Out of Memory error then RAM is insufficient on your machine so use following command
		$ python main_disk.py
		

	- Open another terminal to test queries: (This is necessary for redirecting output into another file)
	- Run following command with file containing queries for testing
		$ python query.py < test_queries.txt
		- This will produce output on standard terminal


	- For HTML Interface open index.html file

***************
For File Structure, see Description.txt

**************
Auto Complete:

	- Auto complete four files as listed above. Firstly using uni.py bi.py and try.py we generate all unigrams bi-grams and tri-grams	respectively from the Corpus (which are SentiWordNet.txt and big.txt) and stores them in test.txt file in decreasing order of their popularity in corpus.
	- tst.py file read this corpus and generate appropriate tri structure to server requests.
	- We had very limited Corpus of English Text to train our Data Structure. Larger the corpus you will have better suggestion for completing phrase.
	- We have supported upto tri-grams.
	- on running tst.py it will open a server socket on specified port given as argument and will server requests for suggestions on that port.
		$ python tst.py 5000

	Note: This will take sometime as it loads data into memory and Construct the data structure.


****************
Spell Suggestion:

	Spell Suggestion contain two files as described above.
	Working of spell suggestion:
		- It reads all the data from corpus and make dictionary of words.
		- query is a single word
		- For a given query, we find all the words which are very 1 levenstein distance away. If any one of them is proper dictionary word then we are done with it. Otherwise we find all valid dictionary words which are two levenstein distance away from query and are valid words. We return the most frequent word from all possible word.
		- This is very fast and we tested well.

****************
Media

	Media folder contains the CSS and Javascript files for UI of webpage.


***************
Main.py

	Main code which starts all the services.
	Then option index.html and perform your queries.
	Note: Wait for sometime until all loading of files are completed.


****************
index.html

	Main file which is interface for performing query. On the left side there are three port options.
	Please make sure you enter the same port numbers on the index.html and when you run the main.py


****************
HelloLucene

			Contains main Lucene code which search for a similar queries
