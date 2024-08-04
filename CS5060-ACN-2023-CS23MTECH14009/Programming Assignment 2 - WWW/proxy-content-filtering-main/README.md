
# ACN Client-Proxy-Server Programing Assignment with Extension-3

Name  : Mayuresh Rajesh Dindorkar  
Roll No : CS23MTECH14007  

Name  : Popat Raj Rameshkumar  
Roll No : CS23MTECH14009 

Name  : Trishita Saha  
Roll No : CS23MTECH14016 

Subject : Advanced Computer Networks (CS50060)
ACN Programming Assignment-2  
---

Assignment is divided into 4 parts as:  

Part 1 Client -> Webserver (Direct Connection):
  
    1. Run server in first container, using below command:  
       python3 Server.py
    2. Run client in second container, using below command:  
       python3 Client.py <serverIP> <serverPort> <resource_url>
       eg.: python3 Client.py 127.0.0.1 12000 HelloWorld.html

Part 2 Client -> Proxy -> Webserver (Indirect Connection):
  
    1. Run server in first container, using below command:  
       python3 Server.py
    2. Run proxy in second container, using below command:  
       python3 Proxy.py
    3. Run client in third container, using below command:  
       python3 Client.py <serverIP> <serverPort> <proxyIP> <proxPort> <resource_url>
       eg.: python3 Client.py 127.0.0.1 12000 127.0.0.1 13000 HelloWorld.html

Part 3 Client -> ExtendedProxy -> Webserver (Indirect Connection):
  
    1. Run server in first container, using below command:  
       python3 Server.py
    2. Run extended proxy in second container, using below command:  
       python3 ExtendedProxy.py
    3. Run client in third container, using below command:  
       python3 Client.py <serverIP> <serverPort> <proxyIP> <proxPort> <resource_url>
       eg.: python3 Client.py 127.0.0.1 12000 127.0.0.1 13000 HelloWorld.html

Part 4 Browser -> ExtendedProxy / Proxy -> Online Webserver (Indirect Connection):
  
    1. Run proxy in a container, using below command: 
       python3 Proxy.py  
       OR  
       To see content filtering in browser, run extended proxy in a container, using below command: 
       python3 ExtendedProxy.py
       
    2. Hit any valid 'http' URL in browser.
       e.g: http://www.example.com

    3. To see user statistics
       python3 Show_browsing_activities.py

VM related commands:  
    
    1. Command used to enter into VM:   
       ssh ubuntu@<VM_IP_Address>

    
    2. To run the container in vm
       lxc exec alice1 -- /bin/bash

    3. To see all containers running in VM:   
       lxc lm

