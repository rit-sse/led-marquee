from datetime import datetime

def get():
	"""
	Get string representation of the current time

	Return: String "HH:MM PM"
	"""
	return datetime.now().strftime("%I:%M %p")

def isFiltered():
    """
    Returns True if it must be filtered, False otherwise.
    """
    return False
