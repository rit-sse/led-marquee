#!/usr/bin/python

#from imapwatcher import ImapWatcher
from telnetwatcher import TelnetWatcher
from marqueewriter import MarqueeWriter
from webserver import WebServer, marquee
from BaseHTTPServer import HTTPServer
from threading import Thread

GmailUsername = "ssemarquee"
GmailPassword = "9e5awrES"

class WebThread(Thread):

        def __init__(self):
                Thread.__init__(self)
                self.server = HTTPServer(('', 80), WebServer)
                print("> Initializing WebThread")

        def run(self):
                try:
                        print("> Listening for Web messages")
                        self.server.serve_forever()
                except KeyboardInterrupt:
                        print("> ^C received, shutting down server")
                        self.server.socket.close()

        def OMGINEEDTODIE(self):
                self.server.shutdown()
                
                    

if __name__ == '__main__':
        
	print 'SSE Marquee Interface'
	print '-----------------------'
	
	#imap = ImapWatcher(marquee, GmailUsername, GmailPassword) This was causing it not to run...
	#imap.start()

	print '> Listening for email...'

	telnet = TelnetWatcher(marquee, '0.0.0.0', 800)
	telnet.start()

	print '> Listening for telnet connections...'

	marquee.start()

	server = WebThread()
	server.start()
        

        ####
        # Right now the web server blocks.  Look into making it a thread.
        ####

        print ''
        print 'Enter a message to send to the marquee'
        print 'or type \'q\' to quit'
        print ''

	

	input = ''
	while not input == 'q':
		input = raw_input('Enter a message: ')
		if input == 'q':
			server.OMGINEEDTODIE()
		else:
			marquee.queueMessage(input.upper())
			
            

	server.join()
	
	#imap.kill()
	#imap.imap.CLOSE()
	#imap.imap.LOGOUT()
	telnet.kill()

	marquee.kill()
