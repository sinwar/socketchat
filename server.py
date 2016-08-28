#!/usr/bin/python           # This is server.py file

# import socket for networking
import socket
# import time               
import time

# create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
# get local machine hostname     
host = socket.gethostname()
port = 12346      
# bind to socket           
s.bind((host, port))

# a list to store all the addresses of clients
clients = []

# set bool variable quitting to false
quitting = False                

print "server created. Have fun :)" ;

while not quitting:
	try:
		# establish the connection with client and recieve data on server in buffer of 1024
		data, addr = s.recvfrom(1024)
		if "Quit" in str(data):
			quitting = True
		if addr not in clients:
			clients.append(addr)

		print time.ctime(time.time()) + str(addr) + ": :" + str(data)
		for client in clients:
			s.sendto(data, client)

	except:
		pass

# close the server connection
s.close()

