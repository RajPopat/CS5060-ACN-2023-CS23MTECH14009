import socket
import threading
from urllib.parse import urlparse
import csv
import datetime

PROXY_IP = '127.0.0.1'
PROXY_PORT = 13000

black_listed_domains=[
    "pirateproxy-bay.com",
    "popcorntime.pro",
    "guns.com",
    "weapons-universe.com",
    "itsecgames.com"
] 
bad_word_list = [
    "Events",
    "Clubs",
    "Internships",
    "Career",
    "Student",
    "News",
    "Alumni",
    "Social",
    "Media",
    "Contact",
    "simple",
    "Example",
    'University'
]

def write_to_csv(record):
    with open('client_activity.csv', 'a+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_file.seek(0)
        is_empty = not csv_file.read(1)
        if is_empty:
            csv_writer.writerow(['ClientIP', 'URL', 'TimeStamp','IsUrlBlocked'])
        csv_writer.writerows(record)
    print('client_activity Saved successfully')

################ Code for Comtent Filtering ###############
def censor_text(original_text, bad_word_list):
    censored_text = original_text
    for bad_word in bad_word_list:
        censored_text = censored_text.replace(bad_word, len(bad_word)*'X')
    return censored_text
###########################################################

def parse_url(url):
    # Parse the URL
    parsed_url = urlparse(url)
    return parsed_url.scheme, parsed_url.netloc, parsed_url.path

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

            requestHeaderlines = request_data.split('\r\n')
            if len(requestHeaderlines) < 1:
                response = "HTTP/1.0 400 Bad Request\r\n\r\nPlease provide valid request".encode()
                self.clientProxySocket.send(response)
                return

            requestLine = requestHeaderlines[0]
            print('Recieved request from client/browser:',requestLine)
            request_line_list = requestLine.split(' ')
            if len(request_line_list) < 3:
                response = "HTTP/1.0 400 Bad Request\r\n\r\nRequest line is not as per http format".encode()
                self.clientProxySocket.send(response)
                return
            method = request_line_list[0]
            url = request_line_list[1]
            if 'https' in url :
                response = "HTTP/1.0 400 Bad Request\r\n\r\nHTTPS requests are not supported".encode()
                self.clientProxySocket.send(response)
                return
            if method != 'GET':
                response = "HTTP/1.0 400 Bad Request\r\n\r\nHTTPS requests are not aaaaa supported".encode()
                self.clientProxySocket.send(response)
                return

            scheme, domain, path = parse_url(url)
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
                serverPort = int(hostLine.split(':')[2].strip())
            else:
                serverPort = 80    
            
            if serverPort == 443 :
                response = "HTTP/1.0 400 Bad Request\r\n\r\nHTTPS requests are not supported".encode()
                self.clientProxySocket.send(response)
                return

            is_good_url=True
            for blocked_domain in black_listed_domains:
                if blocked_domain in url:
                    is_good_url=False       
                    break
            
            #Saving single recored to csv
            write_to_csv([[self.clientAddress[0],url,datetime.datetime.now(),not is_good_url]])

            if not is_good_url:
                # Extension usecase: The url is blocked
                self.clientProxySocket.sendall("HTTP/1.0 403 Forbidden\r\n\r\nSite is blocked by admin".encode())
            else:
                # Proxy to server TCP connection
                proxyServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                proxyServerSocket.settimeout(2)
                proxyServerSocket.connect((serverIP, int(serverPort)))
                print('Proxy has established connection with webserver:', serverIP, ':', str(serverPort))

                # Sending GET request from proxy to webserver
                if 'HTTP/1.1' in request_data:
                    request = f"GET {url} HTTP/1.1\r\nHost: {serverDomainName}\r\n\r\n"
                else:
                    request = f"GET {url} HTTP/1.0\r\nHost: {serverDomainName}\r\n\r\n"
                
                # There should not be encoded like gzip, etc. Hence not sending any header of name: 'Accept-Encoding'
                proxyServerSocket.send(request.encode())

                response = b""
                try:
                    while True:
                        data = proxyServerSocket.recv(4096)
                        if not data:
                            break
                        response += data
                except:
                    pass
                new_response=response
                try:
                    # Censoring the response
                    response = censor_text(response.decode(), bad_word_list)
                    # print('Response received from Webserver -> Proxy:\n', response)
                    response = response.encode()
                except:
                    # The response like image, etc cannot be decoded into UTF8
                    # print('Response received from server is not decodable')
                    response=new_response

                # Sending the response to Client
                self.clientProxySocket.send(response)
                proxyServerSocket.close()
                print('Proxy has closed the connection with webserver')
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
        print('\n************* TCP Extended Web Proxy *************')
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
        pass
    finally:
        print('--------- ExtendedProxy closed Successfully---------')
        welcoming_socket.close()

if __name__ == '__main__':
    main()
