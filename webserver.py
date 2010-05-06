#Copyright Jon Berg , turtlemeat.com

import inspect
import string,cgi,time,urllib
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from marqueewriter import MarqueeWriter

## TODO: it really sucks that we need to use a global variable
marquee = MarqueeWriter("COM3", 115200)
        #"/dev/ttyUSB0"         on linux

class WebServer(BaseHTTPRequestHandler):

    previous_host = ""
    previous_host_spam = 0

    def __init__(self, one, two, three):
        BaseHTTPRequestHandler.__init__(self, one, two, three)
    
    def do_GET(self):
        try:
            f = open(curdir + sep + "uploadText.html",'rb') 
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
                
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        length= int(self.headers['content-length'])

        #remote_host = self.headers['host']
        remote_host = self.client_address[0]
        print '> Host is: ' + str(remote_host)

        if remote_host == WebServer.previous_host:
            print '> Host is same as before'
            WebServer.previous_host_spam += 1
            print '> spam count is: ' + str(WebServer.previous_host_spam)
        else:
            print '> Host is new'
            WebServer.previous_host_spam = 0
            WebServer.previous_host = remote_host

        if WebServer.previous_host_spam >= 5:
           print '> Spam (Ignoring)'
           return
        
        txt = self.rfile.read(length)
        
        message = ""
        if (urllib.unquote_plus(txt[:7]) == "textTo="):
           message = urllib.unquote_plus(txt[7:]).upper()
        else:
            message = urllib.unquote_plus(txt.upper())

        print '> New web message recieved: ', message
        
        marquee.queueMessage(message)
        
        self.wfile.write((txt[7:]))
        return
