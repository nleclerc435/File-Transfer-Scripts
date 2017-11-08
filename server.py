import socket
import serverinfo

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host, port = serverinfo.address
s.bind((host, port))

print('Server running at: {} | Port: {}\nWaiting for a connection...'.format(host, port))

s.listen(5)

while True:
    c, addr = s.accept()
    print('Got connection from:', addr)
    c.send('Connected to: {} | {}'.format(host,port).encode())
    filename = c.recv(1024).decode()
    with open('/home/pi/MyTransferedFiles/'+filename, 'wb') as f:
        print('Receiving: '+filename)
        while True:
            l = c.recv(1024)
            if not l:
                break
            f.write(l)

    f.close()
    c.close()
