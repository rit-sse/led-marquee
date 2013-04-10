from inputs import InputClock
from inputs import InputConsole
from inputs import InputWeather
import time

def cyclePrint():
	printList = [InputConsole, InputClock, InputWeather]
	while(True):
		for i in printList:
			printStr = i.get()
			if (printStr):
				time.sleep(2)
				print(printStr)


cyclePrint()
