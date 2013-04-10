from inputs import InputClock
from inputs import InputConsole
from inputs import InputWeather
import time

def ledMarquee():
	"""
	Main function for LEDMarquee. Sends properly formatted
	text to hardware for display on the Marquee.

	Current state: Printing as simulation.
	"""
	printList = [InputConsole, InputClock, InputWeather]
	while(True):
		#Iterates through all given commands, printing .get() statements.
		for i in printList:
			printStr = i.get()
			if (printStr):
				time.sleep(2)
				print(printStr)


ledMarquee()
