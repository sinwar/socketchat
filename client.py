#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

import threading
import time

tlock = threading.Lock()
shutdown = False

def receving(name, sock):
	while not shutdown:
		try:
			tlock.acquire()
			while True:
				data, addr = sock.recvfrom(1024)
				print str(data)
		except:
			pass
		finally:
			tlock.release()

# create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
# get local machine hostname     
host = socket.gethostname()
port = 0
# bind to socket           
s.bind((host, port))
s.setblocking(0)
server = (host, 12346)
rt = threading.Thread(target=receving, args=("RecvThread", s))
rt.start()

nickname = raw_input("set a nick name:")
message = raw_input(nickname+" --->")

while message != "quit":
	if message != "":
		s.sendto(nickname + ":" + message, server)
	tlock.acquire()
	message = raw_input(nickname+" --->")
	tlock.release()
	time.sleep(0.2)

shutdown = True
rt.join()
s.close()


