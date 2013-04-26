import configparser
from inputs import InputClock
from inputs import InputConsole
from inputs import InputWeather
from inputs import InputMomentum
from inputs import InputEmail
from filters import profanityfilter
import time

# This is a test to make sure it's running on our RPi.
# It simply tests if we can import quick2wire (our i2c library).
# This *should* fail on all of our computers.
onRPi = True
try:
	import quick2wire.i2c as i2c
except ImportError:
	print("ERROR: quick2wire (i2c) failed to import.")
	print("You're probably not running this on the Raspberry Pi.")
	print("Ignoring...")
	print("")
	onRPi = False

# Uncomment the next line to keep the RPi from sending over i2c.
# onRPi = False


def isFamilyFriendly():
	try:
		config = configparser.ConfigParser()                                        
		config.read('config.ini')                                                  

		FAMILY_FRIENDLY = config['FILTERS']['FamilyFriendlyMode']
	except:
		print('ERROR: Config error. Does "config.ini" exist in this directory?')
		print("Exiting...")
		exit()

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
			printStr = i.get().strip()
			if (printStr):
				time.sleep(2)
				if (i.isFiltered()):
					cleanStr = pro.replaceProfanity(printStr)
					if(isFamilyFriendly()):
						if(printStr != cleanStr):
							printStr = "[Message Redacted]"
					else:
						printStr = cleanStr
				if(printStr != ""):
					sendArd(printStr)
					print(printStr)

def sendArd(sendStr):
	global onRPi
	if (onRPi):
		address = 0x04
		byteList = []
		for i in sendStr:
			byteList.append(ord(i))
		byteList.append(0x0A)

		with i2c.I2CMaster() as bus:    
			bus.transaction(
			i2c.writing(address, bytes(byteList)))



ledMarquee()
