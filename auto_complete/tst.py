"""

Execute in the following order --
1. uni.py  ==  Store Unigram model of tokens in desc. order of freq. in test.txt
2. bi.py   ==  Store Bigram model of tokens in desc. order of freq. in test.txt
3. tri.py  ==  Store Triigram model of tokens in desc. order of freq. in test.txt
4. tst.py  == Autocompleting queries


Implementation of Ternary Search Tree data structure for
autocompleting queries. To be run with 'test.txt' as the
argument.

"""

import socket
import sys
HOST = "localhost"
PORT = 5002

results = []
class Node:
    # Constructor for Node Object
    def __init__(self,ch,flag): 
        self.ch = ch
        self.flag = flag
        self.left = 0
        self.right = 0
        self.center = 0                    

    # Function to add a string 
    def Add(self,string,node): 
        key = string[0] 
        
        if node == 0 :
            node = Node(key,0) 

        if key < node.ch :          
            node.left = node.Add(string,node.left)  

        elif key > node.ch :          
            node.right = node.Add(string,node.right)

        else :  
            if len(string) == 1 :
                node.flag = 1  
            else : node.center = node.Add(string[1:],node.center)
            
        return node    

    # DFS for Ternary Search Tree
    def spdfs(self,match):  
        if len(results) > 10:
            return
        if self.flag == 1 : 
            results.append(match)
            print("Match : ",match)
            
        if self.center == 0 and self.left == 0 and self.right == 0:            
            return  
                         
        if self.center != 0 :            
            self.center.spdfs(match + self.center.ch)
            
            
        if self.right != 0 :         
            self.right.spdfs(match[:-1]+self.right.ch)            
            
        if self.left != 0 :            
            self.left.spdfs(match[:-1]+self.left.ch)  


    # Function to search a string in the Ternary Search Tree
    def simple(self,string):  
        temp = self
        i=0
        while temp != 0 :
            if (string[i] < temp.ch) :  temp = temp.left;
            elif(string[i] > temp.ch) : temp = temp.right;
            else :
                i=i+1              
                if(i == len(string)):
                    return temp.flag 
                temp = temp.center

        return 0
            
    
    # Function to implement Auto complete search
    def search(self,string,match):
        if len(results) > 10:
            return

        if len(string) > 0:
            key = string[0]

            if key < self.ch :
                if(self.left == 0):
                    print("No Match Found")
                    return                           
                self.left.search(string,match)

            elif key > self.ch :
                if(self.right == 0):
                    print("No Match Found")
                    return
                self.right.search(string,match)
            else :                
                if len(string) == 1:                                         
                    #if self.flag == 1 : results.append(match+self.ch)
                    if self.center != 0 :
                        self.center.spdfs(match+self.ch+self.center.ch)
                    return
                if self.center != 0:
                    self.center.search(string[1:],match+key)
        else :
            print("Invalid String")
        return


#Parse the Input Dictionary file(test.txt) and build the TST
def fileparse(filename,node):
   
    fd = open(filename)    
    line = fd.readline().strip('\r\n') 
    while line !='':
        
        node.Add(line,node)
        line = fd.readline().strip('\r\n')

digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
def get_query(reqData):
    reqData = reqData[5:]
    lengthStr = ""
    i = 0
    while(reqData[i] in digits):
        lengthStr += reqData[i]
        i += 1
    i+=1
    reqData = reqData[i:]
    length = int(lengthStr)
    query = reqData[:length+1]
    tokens = query.split("+")
    ans = tokens[0]
    for token in tokens[1:]:
        ans += " " + token
    return ans

def toString():
    if len(results) == 0:
        return "[]"
    ans = "[\"" + results[0] + "\""
    for i in range(1,min(8,len(results))):
        ans += ",\"" + results[i] + "\""
    ans += "]"
    return ans

def serve_request(rt):
    print "Starting Auto Complete server on port : " + str(PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print "Auto Completion service started on port: " + str(PORT)
    while 1:
        global results
        conn, addr = s.accept()
        reqData = conn.recv(2048)
        #print reqData
        if (len(reqData) < 5) or (reqData[5] not in digits):
            conn.close
            continue
        query = get_query(reqData)
        results = list()
        root.search(query, '')
        resultStr = toString()
        response = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nConnection: Close\r\nContent-Type: text/html\r\nContent-Length: " + str(len(resultStr)) + "\r\n\r\n" + resultStr;
        print "*** Auto Completion Request ***"
        print "Query: " + query
        print "ResultStr: " + resultStr
        #print "Response: " + response
        print "\n\n\n"
        conn.send(response)
        conn.close()


if __name__=='__main__':    
    root = Node('',0)
    global PORT
    PORT = int(sys.argv[1])
    # Give the Path to the Dictionary File
    Path_to_dict = "auto_complete/test.txt"
    print "Loading dictionary for auto completition . . . "
    fileparse(Path_to_dict,root)
    print "Loading Complete!"
    
    serve_request(root)
    '''
    inp = ''
    while inp !='q':
        inp = raw_input("Enter Query : ",)
        global resultStr
        results = list()
        root.search(inp,'')
        print results
    '''
