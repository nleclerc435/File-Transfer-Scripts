import socket
import os
from threading import Thread

def send_file(ip,port,path):
    print(ip + '|' + str(port))
    s = socket.socket()
    s.connect((ip,port))
    print(s.recv(1024).decode())
    filename = os.path.basename(path)
    print(f'Sending{filename}')
    f = open(path, 'rb')
    s.send(filename.encode())
    l = f.read(1024)
    while(l):
        s.send(l)
        l = f.read(1024)
    s.close()

def dispatch(ip,port,file):
    t = Thread(target=send_file, args=(ip,port,file))
    t.start()