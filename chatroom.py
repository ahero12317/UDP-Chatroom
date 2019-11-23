import socket
import threading
import queue
import sys
import random
import os
from pip._vendor.distlib.compat import raw_input



def RecvDataClient(sock):
    while True:
        try:
            data,addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            pass

if sys.argv[1]=='client':
    
    port = sys.argv[2]
    port=int(port)
    print(' Port->'+str(port))
    server = ('127.0.0.1',5000)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('127.0.0.1',port))

    name = sys.argv[3]
    print('Welcome:'+name)   
    s.sendto(name.encode('utf-8'),server)
    threading.Thread(target=RecvDataClient,args=(s,)).start()
    while True:
        text = ""
        stopword = "send"
        while True:
            data = raw_input()
            if data.strip() == stopword:
                break
            text += "%s\n" % data            
        text = '['+name+']' + '->'+ text
        s.sendto(text.encode('utf-8'),server)
    s.sendto(text.encode('utf-8'),server)
    s.close()
    os._exit(1)




def RecvDataServer(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        
        recvPackets.put((data,addr))
        
if sys.argv[1]=='server':
    port = 5000
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('127.0.0.1',port))
    clients = set()
    recvPackets = queue.Queue()
    print('Server Running...')
    threading.Thread(target=RecvDataServer,args=(s,recvPackets)).start()
    while True:
        while not recvPackets.empty():
            data,addr= recvPackets.get()
            if addr not in clients:
                clients.add(addr)
                continue
            clients.add(addr)
            data = data.decode('utf-8')
            print(str(addr)+data)
            for c in clients:
                if c!=addr:
                    s.sendto(data.encode('utf-8'),c)
    s.close()
