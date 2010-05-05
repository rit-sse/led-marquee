"""
Released under the MIT/X11 License

Copyright (c) 2010 -- Chris Kirkham

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
"""

__version__ = '0.1'
__author__  = 'Chris Kirkham'
__URL__	    = 'http://hmmtheresanidea.blogspot.com'
__credits__ = """
	* Tim's Weblog - http://blog.hokkertjes.nl/2009/03/11/python-imap-idle-with-imaplib2/ - 
	this was a great help. It got me on the right track. It taught me the Event() stuff as 
	well, so that was good.

	* Piers Lauder - http://www.cs.usyd.edu.au/~piers/python/imaplib.html - for imaplib2 
	and the documentation alongside it. Couldn't have done it without him! Thanks!
"""
__license__ = "MIT/X11"
__version__ = "1.0.1"


import threading, imaplib2, os, sys, getpass

DEBUG = False
ServerTimeout = 29 # Mins  (leave if you're not sure)

"""
The worker class for the thread. Letting a thread wait for the server to send something allows the
main thread (if that's what you call it??) to be used for other stuff -- waiting for UI, for example.
"""
class ImapWatcher(threading.Thread):
		
	imap = imaplib2.IMAP4_SSL("imap.gmail.com") # can be changed to another server if needed

	
	stopWaitingEvent = threading.Event()
	#Now, this stopWaitingEvent thing -- it really does make the whole thing work. Basically, 
	#it holds a boolean value which is set and cleared using, oddly enough, the methods set() and
	#clear(). But, the good thing about it is that it has another method, wait(), which holds 
	#execution until it has been set(). I cannot thank threading.Event() enough, I really couldn't
	#have done it without you!
	
	knownAboutMail = [] # will be a list of IDs of messages in the inbox
	killNow = False # stops execution of thread to allow propper closing of conns.
	
	
	"""
	Initialise (sorry, I'm from the UK) everything to get ready for PUSHed mail.
	"""
	def __init__(self, marquee, GMailUsername, GMailPassword):
		
		debugMsg('DEBUG is ENABLED')
		debugMsg('__init__() entered')

		self.marquee = marquee
				
		try:
			#establish connection to IMAP Server
			self.imap.LOGIN(GMailUsername, GMailPassword)

			self.imap.SELECT("SMS Messages")
			
			#get the IDs of all messages in the inbox and put in knowAboutMail
			typ, data = self.imap.SEARCH(None, 'ALL')
			self.knownAboutMail = data[0].split()
			
			#now run the inherited __init__ method to create thread
			threading.Thread.__init__(self)
			
		except: #Uh Oh, something went wrong
			print 'ERROR: IMAP Issue. It could be one (or more) of the following:'
			print '- The impalib2.py file needs to be in the same directory as this file'
			print '- You\'re not connected to the internet'
			print '- Google\'s mail server(s) is/are down'
			print '- Your username and/or password is incorrect'
			sys.exit(1)
			
		debugMsg('__init__() exited')
		
		
	"""
	The method invoked when the thread id start()ed. Enter a loop executing waitForServer()
	untill kill()ed. waitForServer() can, and should, be continuously executed to be alerted
	of new mail.
	"""
	def run(self):
		debugMsg('run() entered')	
		
		#loop until killNow is set by kill() method
		while not self.killNow:
			self.waitForServer()
			
		debugMsg('run() exited')
			
	
	def notify(self, message):
		debugMsg('notify() entered')
		
		print '> New mail message recieved: ', message
		if len(message) > 2:
			self.marquee.queueMessage(message[0:(len(message) - 2)].upper())
		
		debugMsg('notify() exited')
	
	
	"""
	Name says it all really: get (just) the specified header fields from the server for the 
	specified message ID.
	"""
	def getMessageHeaderFieldsById(self, id, fields_tuple):
		debugMsg('getMessageHeaderFieldsById() entered')
		
		#get the entire header
		typ, header = self.imap.FETCH(id, '(RFC822.HEADER)')
		
		#get individual lines
		headerlines = header[0][1]	#.splitlines()
		
		#get the lines that start with the values in fields_tuple
		results = {}
		for field in fields_tuple:
			results[field] = ''
			for line in headerlines:
				if line.startswith(field):
					results[field] = line
					
		debugMsg('getMessageHeaderFieldsById() exited')

		return results #which is a dictionary containing the the requested fields
	

	def getMessageById(self, id):
		debugMsg('getMessageById() entered')
		
		#get the entire header
		typ, header = self.imap.FETCH(id, '(body[text])')
		
		#get individual lines
		headerlines = header[0][1]

		debugMsg('getMessageById() exited')

		return headerlines
	

	"""
	The main def for displaying messages. It draws on getMessageHeaderFieldsById() and growlnotify()
	to do so.
	"""
	def showNewMailMessages(self):
		debugMsg('showNewMailMessages() entered')
		
		#get IDs of all UNSEEN messages 
		typ, data = self.imap.SEARCH(None, 'UNSEEN')
		
		debugMsg('data - new mail IDs:')
		debugMsg(data, 0)
		
		for id in data[0].split():
			if not id in self.knownAboutMail:
				
				#get From and Subject fields from header
				#headerFields = self.getMessageHeaderFieldsById(id, ('From', 'Subject'))
				
				message = self.getMessageById(id)
				
				#notify
				self.notify(message)
				
				#add this message to the list of known messages
				self.knownAboutMail.append(id)
				
		debugMsg('showNewMailMessages() exited')


	"""
	Called to stop the script. It stops the continuous while loop in run() and therefore
	stops the thread's execution.
	"""
	def kill(self):
		self.killNow = True # to stop while loop in run()
		self.timeout = True # keeps waitForServer() nice
		self.stopWaitingEvent.set() # to let wait() to return and let execution continue


	"""
	This is the block of code called by the run() method of the therad. It is what does all 
	the waiting for new mail (well, and timeouts).
	"""
	def waitForServer(self):
		debugMsg('waitForServer() entered')
		
		#init
		self.newMail = False
		self.timeout = False
		self.IDLEArgs = ''
		self.stopWaitingEvent.clear()
		
		def _IDLECallback(args):
			self.IDLEArgs = args
			self.stopWaitingEvent.set()
			#_IDLECallack() is entered when the IMAP server responds to the IDLE command when new
			#mail is received. The self.stopWaitingEvent.set() allows the .wait() to return and
			#therefore the rest of waitForServer().
			
			
		#attach callback function, and let server know it should tell us when new mail arrives	
		self.imap.idle(timeout=60*ServerTimeout, callback=_IDLECallback)

		#execution will stay here until either:
		# - a new message is received; or
		# - the timeout has happened 
		#   	- we set the timout -- the RFC says the server has the right to forget about 
		#	  	  us after 30 mins of inactivity (i.e. not communicating with server for 30 mins). 
		#	  	  By sending the IDLE command every 29 mins, we won't be forgotten.
		# - Alternatively, the kill() method has been invoked.
		self.stopWaitingEvent.wait()
		
		#self.IDLEArgs has now been filled (if not kill()ed)
		
		if not self.killNow: # skips a chunk of code to sys.exit() more quickly.
			
			if self.IDLEArgs[0][1][0] == ('IDLE terminated (Success)'):
			# This (above) is sent when either: there has been a timeout (server sends); or, there
			# is new mail. We have to check manually to see if there is new mail. 
				
				typ, data = self.imap.SEARCH(None, 'UNSEEN') # like before, get UNSEEN message IDs
				
				debugMsg('Data: ')
				debugMsg(data, 0)
				
				#see if each ID is new, and, if it is, make newMail True
				for id in data[0].split():
					if not id in self.knownAboutMail:
						self.newMail = self.newMail or True
					else:
						self.timeout = True 
						# gets executed if there are UNSEEN messages that we have been notified of, 
						# but we haven't yet read. In this case, it response was just a timeout.
						
				if data[0] == '': # no IDs, so it was a timeout (but no notified but UNSEEN mail)
					self.timeout = True
		
			#now there has either been a timeout or a new message -- Do something...
			if self.newMail:
				debugMsg('INFO: New Mail Received')
				self.showNewMailMessages()
							
			elif self.timeout:
				debugMsg('INFO: A Timeout Occurred')
			
		debugMsg('waitForServer() exited')
			
			

"""
Simple procedure to output debug messages nicely.
"""
def debugMsg(msg, newline=1):
	global DEBUG
	if DEBUG:
		if newline:
			print ' '
		print msg
	


