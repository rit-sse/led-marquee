import InputClock
import InputConsole
import time

def cyclePrint():
	printList = [InputConsole, InputClock]
	while(True):
		for i in printList:
			printStr = i.get()
			if (printStr != ""):
				time.sleep(2)
				print(printStr)


cyclePrint()
