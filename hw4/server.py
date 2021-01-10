import sys
import socket
import pickle
import time
import threading


serverPort = 10080

table = {} # addr : clientid

def make_false(addr) :
    global table
    while True :
        try :
            time.sleep(9)
            table[addr][1] = False
        except :
            break

def check_alive(addr,sv) :
    global table
    try :
        while True :
            time.sleep(30)
            if table[addr][1] == False :
                print(addr, "is disappeared")
                del table[addr]
                for key in table.keys() :
                    msg = {"type" : "disappear", "t" : table}
                    msg = pickle.dumps(msg)
                    sv.sendto(msg,key)
                break
    except :
        return  

def server():
    global table

    sv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sv.bind(('',serverPort))
    
    while True :
        data, addr = sv.recvfrom(1024)
        data = pickle.loads(data)

        #if request is registered
        if data['type'] == "register" :
            table[addr] = [data['clientID'],True]
            print(data['clientID']," : ",addr)
            
            for key in table.keys() :
                #boradcast table to the clients
                msg = {"type":"registered", "t":table}
                sv.sendto(pickle.dumps(msg), key)

            false_thread = threading.Thread(target=make_false,args=(addr,))
            false_thread.setDaemon(True)
            false_thread.start()

            check_thread = threading.Thread(target=check_alive,args=(addr,sv))
            check_thread.setDaemon(True)
            check_thread.start()
     
        elif data['type'] == "deregister" :
            print(table[addr]," is deregistered", addr)
            leaving = table[addr]
            del table[addr]
            for key in table.keys() :
                #boradcast table to the clients
                msg = {"type":"deregistered", "t":table}
                sv.sendto(pickle.dumps(msg), key)
        elif data['type'] == "keep_alive" :
            try :
                table[addr][1] =True
            except :
                continue
        else :
            continue

    sv.close()            


"""
Don't touch the code below
"""
if  __name__ == '__main__':
    server()


