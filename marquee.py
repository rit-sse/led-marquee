#!/usr/bin/python

from imapwatcher import ImapWatcher
from telnetwatcher import TelnetWatcher
from marqueewriter import MarqueeWriter
from webserver import WebServer, marquee
from BaseHTTPServer import HTTPServer

GmailUsername = "ssemarquee"
GmailPassword = "9e5awrES"

if __name__ == '__main__':
        
	print 'SSE Marquee Interface'
	print '-----------------------'
	
	imap = ImapWatcher(marquee, GmailUsername, GmailPassword)
	imap.start()

	print '> Listening for email...'

	telnet = TelnetWatcher(marquee, '0.0.0.0', 800)
	telnet.start()

	print '> Listening for telnet connections...'

	marquee.start()

	try:
                server = HTTPServer(('', 80), WebServer)
                print("> Listening for Web messages")
                server.serve_forever()
        except KeyboardInterrupt:
                print("> ^C received, shutting down server")
                server.socket.close()

        ####
        # Right now the web server blocks.  Look into making it a thread.
        ####

        #print ''
        #print 'Enter a message to send to the marquee'
        #print 'or type \'q\' to quit'
        #print ''

	

	#input = ''
	#while not input == 'q':
	#	input = raw_input('Enter a message: ')

	#	if input != 'q':
	#		marquee.queueMessage(input.upper())
	
	imap.kill()
	imap.imap.CLOSE()
	imap.imap.LOGOUT()
	telnet.kill()

	marquee.kill()
