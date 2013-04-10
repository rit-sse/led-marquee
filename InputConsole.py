import os.path, time

lastModTime = None

def get():
	"""
	For testing purposes only.
	Retrieves line from input.txt

	Return: String
	"""
	global lastModTime

	FILENAME = "input.txt"
	if (time.ctime(os.path.getmtime(FILENAME)) != lastModTime):
		lastModTime = time.ctime(os.path.getmtime(FILENAME))
		lastLine = ""
		with open(FILENAME) as fh:
			for line in fh:
				lastLine = line.strip()
		return lastLine
	return ""