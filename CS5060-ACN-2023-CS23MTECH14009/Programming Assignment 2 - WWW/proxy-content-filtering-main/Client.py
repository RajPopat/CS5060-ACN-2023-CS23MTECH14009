import socket
import sys
from bs4 import BeautifulSoup

def fetch_links(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')
    tags_with_resourceurl = []
    for tag in soup.find_all(['img', 'script', 'link', 'a']):
        if 'src' in tag.attrs or 'href' in tag.attrs:
            tags_with_resourceurl.append(tag)
    print(soup)
    sources=[]
    for tag in tags_with_resourceurl:
        if 'src' in tag.attrs:
            sources.append(tag['src'])
        else:
            sources.append(tag['href'])
    
    print("All the objects reffered in this HTML page:", sources)
    return sources

def fetch_objects(resource_url,serverIP,serverPort,proxyIP=None,proxyPort=None):

    try:
        if proxyIP==None:
            proxyIP=serverIP
            proxyPort=serverPort

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((proxyIP, proxyPort))

        request = f"GET http://{serverIP}:{serverPort}/{resource_url} HTTP/1.0\r\nHost: {serverIP}:{serverPort}\r\n\r\n"
        client_socket.send(request.encode())
        
        response = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            response += data
            #print('Fetched object from its Resource Url:',resource_url,'\n',response,'\n\n') # Will show image in byte form
    except Exception as e:
        print('Error:',str(e))
    finally:
        client_socket.close()



def fetch_from_web_server(serverIP, serverPort, resource_url):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((serverIP, serverPort))
        request = f"GET http://{serverIP}:{serverPort}/{resource_url} HTTP/1.0\r\nHost: {serverIP}:{serverPort}\r\n\r\n"
        client_socket.send(request.encode())
        
        response = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            response += data
        print('Index page fetched:\n', response.decode(),'\n\n')

        objects_links = fetch_links(response.decode())
        for link in objects_links:
            fetch_objects(link,serverIP,serverPort)
    except Exception as e:
        print('Error:',str(e))
    finally:
        client_socket.close()

def fetch_from_web_proxy(serverIP, serverPort, proxyIP, proxyPort, resource_url):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((proxyIP, proxyPort))

        request = f"GET http://{serverIP}:{serverPort}/{resource_url} HTTP/1.0\r\nHost: {serverIP}:{serverPort}\r\n\r\n"
        client_socket.sendall(request.encode())
        
        response = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            response += data
        
        print('Response Proxy -> Client:', response.decode())

        if '200 OK' in response.decode():
            objects_links = fetch_links(response.decode())
            for link in objects_links:
                fetch_objects(link,serverIP,serverPort,proxyIP,proxyPort)
    except Exception as e:
        print('Error:',str(e))
    finally:
        client_socket.close()

if __name__ == "__main__":

    print("Usage: python3 Client.py <serverIP> <serverPort> <resource_url> OR python3 Client.py <serverIP> <serverPort> <proxyIP> <proxPort> <resource_url>")

    if len(sys.argv) == 4:
        serverIP = sys.argv[1]
        serverPort = int(sys.argv[2])
        resource_url = sys.argv[3]
        print('Fetching from webserver....')
        fetch_from_web_server(serverIP, serverPort, resource_url)

    elif len(sys.argv) == 6:
        serverIP = sys.argv[1]
        serverPort = int(sys.argv[2])
        proxyIP = sys.argv[3]
        proxyPort = int(sys.argv[4])
        resource_url = sys.argv[5]
        print('Fetching from webProxy....')
        fetch_from_web_proxy(serverIP, serverPort, proxyIP, proxyPort, resource_url)
    
    else:
        print('Please provide valid command line arguments')
    