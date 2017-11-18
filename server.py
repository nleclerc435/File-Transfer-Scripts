import socket
import serverinfo

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((serverinfo.address))

print('Server running at: {} | Port: {}\nWaiting for a connection...'.format(serverinfo.address[0],serverinfo.address[1]))

s.listen(5)

while True:
    c, addr = s.accept()
    print('Got connection from:', addr)
    c.send('Connected to: {} | {}'.format(serverinfo.address[0],serverinfo.address[1]).encode())
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
