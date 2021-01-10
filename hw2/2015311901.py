from socket import *
from datetime import datetime, timedelta
import os

server_name ="Test server"

severIp = gethostbyname(gethostname())

##소켓 연결
serverSock = socket(AF_INET,SOCK_STREAM)
serverSock.bind((severIp,10080))
serverSock.listen(1)

while True :
    
    #요청 기다림
    connectionSock, addr = serverSock.accept() 
    #request data 처리
    data = connectionSock.recv(1024)

    request_data = data.decode().split()

    print(request_data)

    request_method = request_data[0]
    request_version = request_data[2]
    request_filename = request_data[1]

    files = os.listdir()

    header=""
    #request method    
    if request_method == "GET":
        if request_filename == "/" :
            header += 'HTTP/1.0 200 0K\r\n\r\n'
        elif "Cookie:" not in request_data :
            header +='HTTP/1.0 403 Forbidden\r\n\r\n'
            connectionSock.send(header.encode())
            continue
        else :
            header += 'HTTP/1.0 200 0K\r\n\r\n'
            
    elif request_method == "POST":
        userdata = request_data[-1].split('&')
        id = userdata[0][3:]
        pw = userdata[1][9:]
        expire = datetime.utcnow() + timedelta(seconds=3)
        expire_string = expire.strftime("%a, %d %b %Y %H:%M:%S GMT")
        header += "HTTP/1.0 200 0K\n"+"credentials=include\n"+ "access-control-expose-headers: Set-Cookie\n"+ "Set-Cookie:id="+id+";"+"Expires="+expire_string+'\r\n\r\n'
    
    #check filename is available
    if request_filename == "/" :
        file = open('./index.html','r')
        attached_file = file.read().encode()
        
    elif request_filename[1:] not in files :
        if header == 'HTTP/1.0 403 Forbidden\r\n\r\n' :
            header = 'HTTP/1.0 403 Forbidden\r\n\r\n'
        else :
            header = 'HTTP/1.0 404 Not Found\r\n\r\n'
        connectionSock.send(header.encode())
        continue

    elif request_filename[-4:] == "html" :
        file = open('.'+request_filename,'r')
        attached_file = file.read().encode()

    else : 
        file = open('.'+request_filename,'rb')
        attached_file = file.read()

    print(header)

    connectionSock.send(header.encode())
    connectionSock.send(attached_file)

