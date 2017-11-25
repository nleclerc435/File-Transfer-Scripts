import socket
import serverinfo
import threading

def run():
    while True:
        c, addr = s.accept()
        with print_lock:
            print('Got connection from:\n', addr)
        clients_list.append(c)
        c.send('Connected to: {} | {}'.format(serverinfo.address[0],serverinfo.address[1]).encode())
        t = threading.Thread(target=receive_file, args=(c,))
        t.start()

def receive_file(client):
    filename = client.recv(1024).decode()
    with open('/home/pi/MyTransferedFiles/'+filename, 'wb') as f:
        with print_lock:
            print('Receiving: \n'+filename)
        while True:
            l = client.recv(1024)
            if not l:
                break
            f.write(l)
    with print_lock:
        print('{} was transfered successfully!'.format(filename))
    f.close()
    clients_list.remove(client)
    client.close()

#List of clients connecting to server
clients_list = []

#Print lock
print_lock = threading.Lock()

#Server socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((serverinfo.address))
s.listen(5)
print('Server running at: {} | Port: {}\nWaiting for a connection...'.format(serverinfo.address[0],serverinfo.address[1]))

#Start waiting for client connection        
run()
