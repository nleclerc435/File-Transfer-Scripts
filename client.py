import socket
import os
from queue import Queue
from threading import Thread, current_thread, Lock
import serverinfo

print_lock = Lock()

def send_file(path):
    with print_lock:
        print('Starting thread : {}\n'.format(current_thread().name))
    s = socket.socket()
    s.connect((serverinfo.address[0],serverinfo.address[1]))
    print(s.recv(1024).decode())
    filename = os.path.basename(path)
    f = open(path, 'rb')
    s.send(filename.encode())
    l = f.read(1024)
    while(l):
        s.send(l)
        l = f.read(1024)
    print('File was sent successfully!')
    s.close()
    with print_lock:
        print('Finished thread : {}\n'.format(current_thread().name))


def worker(q, item):
    while True:
        q.get()
        send_file(item)
        q.task_done()

def thread_start(list, queue):
    for item in list:
        w = Thread(target=worker, args=(q, item))
        w.daemon = True
        w.start()

    for i in range(len(list)):
        queue.put(i)


while True:
    action = input('Do you want to send separate files(s) or files from a single directory(d)?\n')
    if action == 's':

        num = int(input('How many files do you want to transfer?\n'))
        path_list = []
        while True:
            if num > 0:
                for n in range(num):
                    while True:
                        path = input('Please, enter the full path of the file you wish to send: \n').strip('\"')   
                        if os.path.exists(path):
                            size = os.path.getsize(path)
                            print(size)
                            path_list.append(path)
                            print(path_list)
                            break
                        else:
                            print('Path not found! Are you sure you wrote the right path?')
                            continue
                break
            else:
                print('You entered 0. Please enter a valid number.')
                continue


        print(path_list)

        q = Queue()
        thread_start(path_list, q)
        q.join()
        break



    elif action == 'd':
        path = input('Please enter the path for your folder:\n')   
        file_list = [item for item in os.listdir(path) if os.path.isfile(item)]
        print(file_list)
        q = Queue()
        thread_start(file_list, q)
        q.join()
        break

    else:
        print('Command not recognized. Please use "s"(separate files) or "d"(directory).')
        continue
