import imaplib, email, configparser


def get():
	"""
	Returns the properly formatted String grabbed from Email to display
	as SMS output to reader.
	"""

	try:
		config = configparser.ConfigParser()
		config.read('config.ini')

		# See the Google Drive for account and password.
		GMAILUSER = config['EMAIL']['username']
		GMAILPWD  = config['EMAIL']['password']
	except:
		print('ERROR: Config error. Does "config.ini" exist in this directory?')
		print("Exiting...")
		exit()

	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(GMAILUSER, GMAILPWD)
	mail.list()
	# Out: list of "folders" aka labels in gmail.
	mail.select("inbox") # connect to inbox.


	result, data = mail.search(None, "ALL")
	 
	ids = data[0] # data is a list.
	id_list = ids.split() # ids is a space separated string
	if len(id_list) > 0:
		latest_email_id = id_list[-1] # get the latest

		# fetch the email body (RFC822) for the given ID
		result, data = mail.fetch(latest_email_id, "(RFC822)")
		"""
		here's the body, which is raw text of the whole email
		including headers and alternate payloads
		""" 
		raw_email = data[0][1] 

		msg = email.message_from_bytes(raw_email) 
		

		msgStr = msg.__str__()

		smsBeginIndex = msgStr.find("format=flowed; delsp=yes")
		if (smsBeginIndex != -1):
			msgContent = msgStr[(smsBeginIndex + 25) :].strip().splitlines()
			return (" ".join(msgContent).replace("-- Sent using SMS-to-email."
					" Reply to this email to text the sender back and"
					"   save on SMS fees. https://www.google.com/voice/", ""))
	else:
		print("No mail.")

def isFiltered():
	"""
	Returns True if it must be filtered, False otherwise.
	"""
	return True
