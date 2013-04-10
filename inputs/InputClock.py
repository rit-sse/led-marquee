from datetime import datetime

def get():
	"""
	Get string representation of the current time

	Return: String "HH:MM PM"
	"""
	return datetime.now().strftime("%I:%M %p")