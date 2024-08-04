import socket
import threading
from urllib.parse import urlparse

PROXY_IP = '127.0.0.1'
PROXY_PORT = 13000

class MyThread(threading.Thread):

    def __init__(self, clientProxySocket, clientAddress):
        super().__init__()
        self.clientProxySocket = clientProxySocket
        self.clientAddress = clientAddress

    def run(self):
        try:
            # Received request from client
            request_data = self.clientProxySocket.recv(4096).decode()
            #print('Recieved request from client/browser:',request_data)

            # Splitting the received request into request linbe and header lines
            requestHeaderlines = request_data.split('\r\n')
            if len(requestHeaderlines) < 1:
                response = "HTTP/1.0 400 Bad Request\r\n\r\nPlease provide valid request".encode()
                self.clientProxySocket.send(response)
                return 
            
            # Extracting the request line
            requestLine = requestHeaderlines[0]
            print('Recieved request from client/browser:',requestLine)
            request_line_list = requestLine.split(' ')
            if len(request_line_list) < 3:
                response = "HTTP/1.0 400 Bad Request\r\n\r\nRequest line is not as per http format".encode()
                self.clientProxySocket.send(response)
                return
            
            method = request_line_list[0]
            url = request_line_list[1]
             
            if 'https' in url:
                response = "HTTP/1.0 400 Bad Request\r\n\r\nHTTPS requests are not supported".encode()
                self.clientProxySocket.send(response)
                return
            if method != 'GET':
                response = "HTTP/1.0 501 Method Not Implemented\r\n\r\nMethod '" + method + "' is not implemented."
                self.clientProxySocket.send(response.encode())
                return

            # Extracting serverIP and serverPort from GET URL 
            headerLines = requestHeaderlines[1:]
            hostLine = ''
            for line in headerLines:
                if 'Host' in line:
                    hostLine = line
                    break

            serverDomainName = hostLine.split(':')[1].strip()
            serverIP = socket.gethostbyname(serverDomainName)
            if len(hostLine.split(':')) > 2:
                serverPort = hostLine.split(':')[2].strip()
            else:
                serverPort = 80    
            
            # Proxy to server TCP connection
            proxyServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxyServerSocket.settimeout(2)
            proxyServerSocket.connect((serverIP, int(serverPort)))
            print('Proxy has established connection with webserver:', serverIP, ':', str(serverPort))

            # Sending GET request from proxy to webserver
            request = request_data                # Here, encoded response is also fine, because we dont want to parse it 'Accept-Encoding'
            proxyServerSocket.sendall(request.encode())

            try:
                while True:
                    data = proxyServerSocket.recv(4096)
                    if not data:
                        break
                    self.clientProxySocket.sendall(data)
            except socket.timeout:
                 pass
            print('Proxy Successfully received data from server')
            proxyServerSocket.close()
            print('Proxy has closed the connection with webserver:', serverIP, ':', str(serverPort))
        
        except Exception as e:
            response = (f"HTTP/1.0 500 Server error\r\n\r\n{str(e)}").encode()
            self.clientProxySocket.send(response)
            print('Error occurred:', e)
        finally:
            self.clientProxySocket.close()
            print('Proxy has closed connection with client:', self.clientAddress[0],':',self.clientAddress[1])
            print('=============================================================')

def main():
    try:
        print('\n************* TCP Web Proxy *************')
        welcoming_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        welcoming_socket.bind((PROXY_IP, PROXY_PORT))
        welcoming_socket.listen(5)

        print(f'TCP Web Proxy having IP {PROXY_IP} is listening on port {PROXY_PORT}....\n')
        while True:
            clientProxySocket, clientAddress = welcoming_socket.accept()
            print(f'Proxy has established connection with client {clientAddress[0]} : {clientAddress[1]}')
            client_thread = MyThread(clientProxySocket, clientAddress)
            client_thread.start()
    except KeyboardInterrupt:
        print('--------- Proxy is closed ---------')
    finally:
        welcoming_socket.close()

if __name__ == '__main__':
    main()
