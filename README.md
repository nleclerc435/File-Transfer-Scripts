# File-Transfer-Scripts
Basic server/client scripts to transfer files quickly between my PC and my Raspberry Pi

I needed a solution to send small files from my PC to my Rapsberry Pi without using my email or a cloud service everytime. I decided to try
and script a simple solution with Python. This was a good opportunity to learn about networking which I didn't know much about before.

##Please note:
- You can find references to *_serverinfo_* in the code and the file is not part of this repo. It is a separate file that I created to hold the
IP/Port information for my Raspberry Pi. Doing it that way prevented me from accidentally giving out that information in a commit. If someone
wants to use this script, please create your own serverinfo.py and add your IP/port in a tuple variable.

- In the client script, I experimented with threads to see if it would speed up the transfer process. At the moment, I have a thread running
for each file to be sent which is a bit too intense when you start to send a good number of files. This will be optimized at some point.

##Usage
###server.py
This is a basic server script made to run at all time on my Raspberry Pi. It creates a TCP/IP socket, binds it to the Pi's IP address and port
found in the serverinfo.py file. It will then listen and wait for connection. Once a connection is made, it will send a connection confirmation
to the client and then will wait for the name of the file to be received. The server will then create a new empty file with that name in a specific
folder and starts writing the data received from the client to it. Once there is no more byte to be received, it will break and close the file and 
the connection to the client.

###client.py
####Basic logic
The client script will start by asking the user to choose between sending files from different folders or files from a single directory.

In the case of separate files, it will ask for the number of files to be sent and then the path for each file to be sent. If the paths exists,
they will be put in a list. Else, the user will be asked to enter a valid path. Once a list is set, it creates a queue and fills it with as many
workers as there are files to be sent. The same goes for threads that are being created and started for the same amount (*Please read the 'Please note'
part of this file for explanation*). Once the queue is filled with workers, the threads will start sending the files.

For files in a single directory, the logic is about the same as the one above for separate files. The major difference is that instead of asking
for multiple paths, the user will be asked to enter the single directory and the script will loop in that folder to find all files and then add
them to a list.

####More detail
Queue/Workers - Workers will get their 'task' from the queue given to it in the arguments and the use the send_file function to the the item
also given in the arguments when it is called.

Threads - For each item in a list, a new Thread is created and given the worker function as a target. The argument given to that worker will be
the queue used at that time and the item coming from the list. The function will then start the thread and start populating the queue for the
amount of files to be sent.
