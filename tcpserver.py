import threading, socket

class ClientManager(threading.Thread):
	def __init__(self, conn, addr):
		""" Creates a thread to deal with a client connection."""
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.id = self.addr[0] + '/' + str(self.addr[1])

	def run(self):
		"""Thread logic. Receives and processes client messages, sending responses or modifying state."""
		global clients

		clients.append(self.conn)

		conn_alert = 'Connected ' + self.id
		print conn_alert
		self.conn.send('Connected to chat')
		self.conn.send('Users: ' + str(len(clients)))
		for client in clients:
			if client is not self.conn: client.send(conn_alert)

		connected = True
		while connected:
			msg = str(self.conn.recv(1024)).split('\n')
			for line in msg:
				if line != '':
					# logout command
					if '/exit' in line:
						connected = False
						clients.remove(self.conn)
						logout_alert = self.id + ' logged out'
						print logout_alert
						for client in clients:
							if client is not self.conn: client.send(logout_alert)
					# namechange command
					elif '/name' in line:
						index = line.find('/name') + len('/name')
						new_id = line[index:]
						new_id = new_id.strip()
						name_change_alert = self.id + ' is now ' + new_id
						print name_change_alert
						for client in clients:
							client.send(name_change_alert)
						self.id = new_id
					# normal message
					else:
						response = self.id + ' : ' + line
						print response
						for client in clients:
							client.send(response)
		self.conn.close()

if __name__ == '__main__':
	""" Creates a server on port 8080 and starts listening for connections."""
	PORT = 8080
	clients = []

	main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	main_socket.bind(('', PORT))
	main_socket.listen(5)

	print 'Starting server at port ' + str(PORT)

	while True:
		conn, addr = main_socket.accept()
		ClientManager(conn, addr).start()