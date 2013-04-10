from inputs import InputClock
from inputs import InputConsole
from inputs import InputWeather
from filters import profanityfilter
import time, threading, queue

def ledMarquee():
	"""
	Main function for LEDMarquee. Sends properly formatted
	text to hardware for display on the Marquee.

	Current state: Printing as simulation.
	"""

	# Which files to get input from
	printList = [InputConsole, InputClock, InputWeather]

	# Minimum time, in seconds, between updates
	timeOut = 2

	# Display queue
	q = queue.Queue()

	pro = profanityfilter.ProfanityFilter()

	t = threading.Thread(target=updateThread, args=(q, printList, timeOut))
	t.daemon = True
	t.start()

	while(True):
		s = q.get()
		print(pro.replaceProfanity(s))


def updateThread(q, inList, timeOut):
	prevStrDict = {}
	for i in inList:
		prevStrDict[i] = i.get()

	# Iterates through all given commands.
	while (True):
		for i in inList:
			printStr = i.get()
			time.sleep(timeOut)
			# If the .get() command returns nothing or hasn't changed, ignore it.
			if (printStr and prevStrDict[i] != printStr):
				# If it has changed, update the dict and queue.
				prevStrDict[i] = printStr
				q.put(printStr)



ledMarquee()
