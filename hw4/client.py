import sys
import socket
import pickle
import threading
import time
import os
import multiprocessing
import subprocess

serverIP = '10.0.0.3'
serverPort = 10080
clientPort = 10081

table = {}

def sending_keep_alive(cli) :
    while True :
        print("sent kepp_alive message...")
        msg = {"type" : "keep_alive"}
        s = pickle.dumps(msg)
        cli.sendto(s,(serverIP,serverPort))
        time.sleep(9)


def wait_fo_boradcast(cli) :
    global table
    while True :
        res,addr = cli.recvfrom(1024)
        data = pickle.loads(res)
        if data["type"] == "chat" :
            chatting = " ".join(data["text"])
            print("[From]",table[addr][0],"   ",chatting)
        else :
            table= data["t"]
            print("recieved new versions")

def client(serverIP, serverPort, clientID):
    
    global table

    cli = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    cli.bind(('',clientPort))

    #Send registration message
    msg = {"type" : "register","clientID" : clientID, "keep_alive" : True}
    cli.sendto(pickle.dumps(msg),(serverIP,serverPort)) #send client ID    
    msg = cli.recv(1024)
    table = pickle.loads(msg)["t"]

    #waiting thread
    waiting_thread = threading.Thread(target=wait_fo_boradcast, args=(cli,))
    waiting_thread.setDaemon(True)
    waiting_thread.start()

    #sending keep alive in every 10 seconds
    sending_thread = threading.Thread(target=sending_keep_alive,args=(cli,))
    sending_thread.setDaemon(True)
    sending_thread.start()


    while True :
        command = input().split(" ")
        if command[0] == "@show_list" :
            for key in table.keys() :
                print(table[key][0]," ",key[0],":",key[1])
        elif command[0] == "@exit" :
            msg = {"type": "deregister"}
            msg = pickle.dumps(msg)
            cli.sendto(msg,(serverIP,serverPort))
            break
        elif command[0] == "@chat" :
            whom = command[1]
            text = command[2:]
            for key in table.keys() :
                if table[key][0] == whom :
                    whom_addr = key
                    msg = {"type" : "chat", "text" : text}
                    cli.sendto(pickle.dumps(msg),(whom_addr))
        else :
            continue

    return
        

        
            

"""
Don't touch the code below!
"""
if  __name__ == '__main__':

    clientID = input("Enter ID : ")
    client(serverIP, serverPort, clientID)


