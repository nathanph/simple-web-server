#!/usr/local/bin/python

#these are the imports that I needed
import threading
import string
import os
import mimetypes
from socket import *

def worker(connectionSocket):
   while 1:
      sentence = connectionSocket.recv(1024)
      print("sentence", sentence);
      if sentence == b'quit': break
      capitalizedSentence = sentence.upper()
      connectionSocket.send(capitalizedSentence)
   connectionSocket.close()

serverPort = 15000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((gethostname(), serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
while 1:
    (connectionSocket, addr) = serverSocket.accept()
    t = threading.Thread(target = worker, args=(connectionSocket, ))
    t.start()

