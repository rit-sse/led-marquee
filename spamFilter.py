import time

class SpamFilter():
    def __init__(self,toofast, toomany):
        """
        toofast is the time (in seconds) if 'toomany' messages are sent the person will get /" banned /" 
        toomany is the number of messages a person can send in the time frame /" toofast /" 
        
        """
        self.toofast=toofast
        self.toomany=toomany
        self.whoisspaming={}
        self.times={}
    
    
    def check(self,host,message):

        currTime=time.clock()

        if not host in self.whoisspaming:
            self.whoisspaming[host] = [0, [0],0]
            
        self.whoisspaming[host][0] = self.whoisspaming[host][0]+ 1
        times=self.whoisspaming[host][1]
        times.append(currTime)
        self.whoisspaming[host][1]=times

        self.speedSpam(host)
        
        #if the person is blocked return "" if not return the message
        if not self.is_blocked(host):
            return message
        else:
            print "(message spam)"
            return ""
    
    def speedSpam(self,host):
        lenth=len(self.whoisspaming[host][1])
        if lenth>self.toomany:
            t=self.whoisspaming[host][1][lenth-1] - self.whoisspaming[host][1][lenth - self.toomany]

            if t<self.toofast:

                self.whoisspaming[host][2]=self.whoisspaming[host][1][lenth-1]+30

    
    
    
    def msgSpam(self,msg):
        pass
    
    
    
    
    
    
    def is_blocked(self,host):
        #returns true if the person is banned
        return self.whoisspaming[host][2]>time.clock()
    
