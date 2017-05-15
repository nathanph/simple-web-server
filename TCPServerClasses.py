#!/usr/bin/python3

#Here are the imports that I needed.
import threading
import string
import os
import mimetypes
import base64
from socket import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#myThread inherits from threading.Thread
class myThread (threading.Thread):
    # __init__ is the constructor
    # self is the object
    # all instance methods in the class will have self
    # as the first parameter
    def __init__(self, connectionSocket):
        threading.Thread.__init__(self)
        #self causes connectionSocket to be a data member
        self.connectionSocket = connectionSocket


    def build_response(self, request):
        response = ""
        # Send a 400errorDoc.html when we get something other than a GET request.
        if (request.find("GET")==-1):
            response = self.bad_request(request)
        else:
            file_name = request.split('\n',1)[0].split()[1]
            cwd = os.getcwd()
            if(os.path.isfile(cwd + file_name)):
                response = self.ok(request)
            else:
                response = self.not_found(request)
        return response

    def not_found(self, request):
        response=""
        cwd = os.getcwd()
        response_file = cwd+"/404errorDoc.html"
        http_version = "HTTP/1.1 "
        status_code = "404 "
        status_phrase = "Not Found\r\n"
        file_type = mimetypes.guess_type(response_file)[0]
        content_type = "Content-Type: " + file_type + "\r\n"
        file_size = os.path.getsize(response_file)
        content_length = "Content-Length: " + str(file_size) + "\r\n"
        connection = "Connection: close\r\n"
        body=""
        with open(response_file, 'r') as data:
            body += data.read()
        response += http_version + status_code + status_phrase
        response += content_type
        response += content_length
        response += connection
        response += "\r\n"
        response += body

        return response

    def ok(self, request):
        response=""
        file_name = request.split('\n',1)[0].split()[1]
        cwd = os.getcwd()
        response_file = cwd + file_name
        http_version = "HTTP/1.1 "
        status_code = "200 "
        status_phrase = "OK\r\n"
        file_type = mimetypes.guess_type(response_file)[0]
        content_type = "Content-Type: " + file_type + "\r\n"
        file_size = os.path.getsize(response_file)
        content_length = "Content-Length: " + str(file_size) + "\r\n"
        connection = "Connection: close\r\n"
        body=""
        if (file_type.find("text")==-1):
            with open(response_file, 'rb') as data:
                body += base64.b64encode(data.read())
        else:
            with open(response_file, 'r') as data:
                body += data.read()
        response += http_version + status_code + status_phrase
        response += content_type
        response += content_length
        response += connection
        response += "\r\n"
        response += body
        return response

    def bad_request(self, request):
        response=""
        cwd = os.getcwd()
        response_file = cwd+"/400errorDoc.html"
        http_version = "HTTP/1.1 "
        status_code = "400 "
        status_phrase = "Bad Request\r\n"
        file_type = mimetypes.guess_type(response_file)[0]
        content_type = "Content-Type: " + file_type + "\r\n"
        file_size = os.path.getsize(response_file)
        content_length = "Content-Length: " + str(file_size) + "\r\n"
        connection = "Connection: close\r\n"
        body=""
        with open(response_file, 'r') as data:
            body += data.read()
        response += http_version + status_code + status_phrase
        response += content_type
        response += content_length
        response += connection
        response += "\r\n"
        response += body
        return response


    #thread execution starts here
    def run(self):
        print(bcolors.OKGREEN + "Connection established." + bcolors.ENDC)
        message = self.connectionSocket.recv(4096).decode()
        print(bcolors.HEADER + "> REQUEST" + bcolors.ENDC)
        print(message)
        response = self.build_response(message)
        print(bcolors.HEADER + "< RESPONSE" + bcolors.ENDC)
        print(response)
        self.connectionSocket.send(response.encode())
        self.connectionSocket.close()
        print(bcolors.OKGREEN + "Connection closed." + bcolors.ENDC)



def main():
    serverPort = 12056
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((gethostname(), serverPort))
    serverSocket.listen(1)
    print(bcolors.OKBLUE + "===================================" + bcolors.ENDC)
    print(bcolors.OKBLUE + "The server is ready to receive" + bcolors.ENDC)
    print(bcolors.OKBLUE + "Hostname: " + gethostname() + bcolors.ENDC)
    print(bcolors.OKBLUE + "Port: " + str(serverPort) + bcolors.ENDC)
    print(bcolors.OKBLUE + "===================================" + bcolors.ENDC)
    print()
    while 1:
        (connectionSocket, addr) = serverSocket.accept()
        t = myThread(connectionSocket)
        t.start()

if __name__ == "__main__":
    main()
