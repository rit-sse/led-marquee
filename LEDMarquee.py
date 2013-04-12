import quick2wire.i2c as i2c
import configparser
from inputs import InputClock
from inputs import InputConsole
from inputs import InputWeather
from inputs import InputMomentum
from inputs import InputEmail
from filters import profanityfilter
import time

def isFamilyFriendly():
	config = configparser.ConfigParser()                                        
	config.read('config.ini')                                                  

	FAMILY_FRIENDLY = config['FILTERS']['FamilyFriendlyMode']

	if(FAMILY_FRIENDLY == 'YES'):
		return True
	else:
		return False


def ledMarquee():
	"""
	Main function for LEDMarquee. Sends properly formatted
	text to hardware for display on the Marquee.

	Current state: Printing as simulation.
	"""
	printList = [InputConsole, InputClock, InputWeather, InputMomentum, InputEmail]
	FamilyFriendly = isFamilyFriendly()
	pro = profanityfilter.ProfanityFilter()

	while(True):
		#Iterates through all given commands, printing .get() statements.
		for i in printList:
			printStr = i.get()
			if (printStr):
				time.sleep(2)
				if (i.isFiltered()):
					if(isFamilyFriendly()):
						if(printStr != pro.replaceProfanity(printStr)):
							printStr = "[Message Redacted]"
					else:
						printStr = pro.replaceProfanity(printStr)
				sendArd(printStr)
				print(printStr)


def sendArd(sendStr):
	address = 0x04
	byteList = []
	for i in sendStr:
		byteList.append(ord(i))
	byteList.append(0x0A)

	with i2c.I2CMaster() as bus:    
		bus.transaction(
		i2c.writing(address, bytes(byteList)))



ledMarquee()
