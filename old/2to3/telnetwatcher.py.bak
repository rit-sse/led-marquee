
import select
import socket
import serial
import time
import threading
from marqueewriter import MarqueeWriter

class TelnetWatcher(threading.Thread):

	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sendOverride = False

	def __init__(self, marquee, address, port):
		self.marquee = marquee
		self.socket.bind((address, port))
		self.socket.settimeout(1)
		self.killNow = False
		threading.Thread.__init__(self)

	def kill(self):
		self.killNow = True

	def getConnection(self):
		self.socket.listen(1)

		while not self.killNow:
			try:
				conn, addr = self.socket.accept()
				if conn != None:
					conn.settimeout(None)
				return conn
			except socket.timeout:
				pass

	def run(self):
		while not self.killNow:
			conn = self.getConnection()
			
			if conn != None:
				print '> New telnet connection established'

				while not self.killNow:
					# check if there's stuff to read
					try:
						ready_to_read, ready_to_write, in_error = select.select([conn],[],[],0.1)
					except:
						break
		
					# is there new stuff to read?
					if ready_to_read:
						try:
                                                        print conn
                                                        data = conn.recv(1024).replace('\r', ' ')
                                                        print data
                                                        data = data.upper()
                                                        print data

                                                        print marquee
							marquee.queueMessage(data)
						except:
                                                        print 'I am error.'
							break
				
						if not data:
                                                        print 'No data found.'
							break
					
						# actually do something with it
						#if not data == '\n':
							# add to message queue here
			
				print '> Closing telnet connection'
				conn.close()
