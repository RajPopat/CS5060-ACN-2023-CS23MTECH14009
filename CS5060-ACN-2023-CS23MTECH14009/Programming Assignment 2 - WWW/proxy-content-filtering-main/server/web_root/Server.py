from socket import *
import threading
import os
from urllib.parse import urlparse

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12000
ROOT_DIR = 'web_root'

def parse_url(url):
    parsed_url = urlparse(url)
    # return HttpScheme, domainName, resource_url
    return parsed_url.scheme, parsed_url.netloc, parsed_url.path

class MyThread(threading.Thread):

    def __init__(self, clientSocket, clientAddress):
        super().__init__()
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

    def run(self):
        try:
            request_data = self.clientSocket.recv(4096).decode()
            request_lines = request_data.split('\r\n')

            if len(request_lines) < 1:
                response = "HTTP/1.0 400 Bad Request\r\n\r\nPlease provide valid request".encode()
                self.clientSocket.send(response)
                return 
           
            request_line = request_lines[0].split()
            if len(request_line) < 2:
                response = "HTTP/1.0 400 Bad Request\r\n\r\nPlease provide valid request".encode()
                self.clientSocket.send(response)
                return
            
            method = request_line[0]    # method is not used here
            
            if method == 'GET':
                url = request_line[1]

                # Construct the full file path
                HttpScheme, domain, resource_url = parse_url(url)
                resource_url=resource_url.lstrip('/')
                print('Received URL:', url)
                
                # Print the results
                print("HttpScheme:", HttpScheme)
                print("DomainName:", domain)
                print("Resource URL:", resource_url)

                # Check if the requested file exists
                if os.path.isfile(resource_url):
                    with open(resource_url, 'rb') as file:
                        response_data = file.read()
                    response = f"HTTP/1.0 200 OK\r\n\r\n".encode() + response_data
                else:
                    response = "HTTP/1.0 404 Not Found\r\n\r\nFile not found. Please check the resource URL".encode()
            else:
                res = "HTTP/1.0 501 Method Not Implemented\r\n\r\nMethod '" + method + "' is not implemented."
                response = res.encode()
            self.clientSocket.send(response)
        except Exception:
            pass
        finally:
            self.clientSocket.close()
            print('Closed the connection with client:', self.clientAddress[0])
            print('=============================================================')

def main():

    try:
        print('\n************* TCP Web Server *************')
        welcoming_socket = socket(AF_INET, SOCK_STREAM)
        welcoming_socket.bind((SERVER_IP, SERVER_PORT))
        welcoming_socket.listen(5)

        print(f'TCP Server having IP {SERVER_IP} is listening on port {SERVER_PORT}....\n')
        print('=============================================================')
        
        while True:
            socketForClient, clientAddress = welcoming_socket.accept()
            print(f'Established connection with client {clientAddress[0]} : {clientAddress[1]}\n')
            client_thread = MyThread(socketForClient, clientAddress)
            client_thread.start()
    
    except KeyboardInterrupt:
        pass
    
    finally:
        welcoming_socket.close()

if __name__ == '__main__':
    main()
