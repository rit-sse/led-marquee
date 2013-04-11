import quick2wire.i2c as i2c

from inputs import InputClock
from inputs import InputConsole
from inputs import InputWeather
from inputs import InputMomentum
from inputs import InputEmail
from filters import profanityfilter
import time



def ledMarquee():
	"""
	Main function for LEDMarquee. Sends properly formatted
	text to hardware for display on the Marquee.

	Current state: Printing as simulation.
	"""
	printList = [InputConsole, InputClock, InputWeather, InputMomentum, InputEmail]

	pro = profanityfilter.ProfanityFilter()

	while(True):
		#Iterates through all given commands, printing .get() statements.
		testSend("this")
		for i in printList:
			printStr = i.get()
			if (printStr):
				time.sleep(2)
				if (i.isFiltered()):
					printStr = pro.replaceProfanity(printStr)
				sendArd(printStr)
				print(printStr)


def sendArd(sendStr):
	address = 0x04
	print("test")
	byteList = []
	for i in sendStr:
		byteList.append(ord(i))
	byteList.append(0x0A)

	with i2c.I2CMaster() as bus:    
		bus.transaction(
		i2c.writing(address, bytes(byteList)))

sendArd("test")
ledMarquee()
