
import select
import serial
import time
import threading
from profanityfilter import *

class MarqueeWriter(threading.Thread):

	def __init__(self, port, baud):
		self.serial = serial.Serial(port, baud)
		self.messageQueue = list()
		self.queueLock = threading.Lock()
		self.scrollMode = True
		self.lastTime = ''
		self.killNow = False
		self.prof = ProfanityFilter()

		threading.Thread.__init__(self)

	def queueMessage(self, message):
		self.queueLock.acquire()
		self.messageQueue.append(message)
		self.queueLock.release()

	def clearQueue(self):
		self.messageQueue = list()

	def kill(self):
		self.killNow = True

	def run(self):
		while not self.killNow:
			self.processMessages()

	def processMessages(self):
		# print any queued messages
		while len(self.messageQueue) > 0:

			# pop the message off the queue
			self.queueLock.acquire()
			message = self.messageQueue.pop(0)
			self.queueLock.release()

			message = message.strip()

                        # If message is only spaces or invalid, continue
			if message == '' or message == None:
                                continue

			# if message is spam -- i.e. HUGE, ignore it
			if ( len(message) > 75 ):
                                print 'message too long'
                                continue

                        
			# enable scroll mode for messages
			if not self.scrollMode:
				self.scrollMode = True
				self.serial.write('b')

			



			message = self.prof.replaceProfanity(message).upper()
			
			length = 0
			if ( len(message) < 75 ):
                                length = len(message)
                        else:
                                length = 75
                                
			message = message[0:length]

			message = message + "   "

			# actually do something with it
			data = ''
			
			while not (data == '\n') and (len(message) > 0):
				data = message[0]
				message = message[1:len(message)]

				self.serial.write(data)
				response = self.serial.read()
				
				if not response == 'n':
					continue


		# send time
		if self.scrollMode:
			self.scrollMode = False
			self.sendOverride = True
			self.serial.write('a')
			time.sleep(.5)

		currTime = time.strftime("%I:%M")
		if self.sendOverride or not self.lastTime == currTime:
			self.serial.write('z')            
			self.serial.write(currTime + "\n")
			self.lastTime = currTime
			self.sendOverride = False
