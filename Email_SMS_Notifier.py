# Rachel Friedman 
# 8/4/13

import imaplib, smtplib, time, email, textwrap

class Email_SMS_Notifier():
	""" Notifies by SMS of important Gmail emails """
	def __init__(self, username, password, restTime, maxTexts, phoneAddr):
		self._connection = imaplib.IMAP4_SSL("imap.gmail.com", "993") # new connection
		self._connection.login(username, password) # login with username and password
		self._messageLst = []
		self._restTime = restTime
		self._maxTexts = maxTexts
		self._username = username
		self._password = password
		self._phone = phoneAddr

	def checkMail(self):
		""" Checks the mailbox for new important emails """ 
		self._connection.select("[Gmail]/Important", readonly = True) # only look at emails marked important and don't mark things read after looking at them
		messages = self._connection.search(None, 'UNSEEN')[1][0].split() # only report back on unread emails

		for message in messages:
			if message not in self._messageLst: # if not already reported
				_ , data = self._connection.fetch(message, '(RFC822)')
				mail = email.message_from_string(data[0][1]) # convert to email format
				text = ""

				for part in mail.walk():
					if part.get_content_type() == "text/plain":
						text = part.get_payload(decode=True) # gets plain text from email 

				self._messageLst.append(message)
				sender = mail["From"].split("<")[0].rstrip() # gets name of sender without the email address
				subject = mail["Subject"]
				self.notify([("New message from " + sender + ". SUBJECT - " + subject + " MESSAGE - " + text).rstrip()])

	def notify(self, message):
		""" Send notification text message with email details """
		if len(message[0]) > 160: # if the message is greater than 160 characters, need to split it up into multiple texts
			message = textwrap.wrap(message[0], 160)

		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(self._username, self._password) # login with username and password to send SMS

		sentCount = 0

		for part in message: # message is a list of message strings (under 160 characters each)
			if sentCount == self._maxTexts: # make sure not too many texts are sent for large emails
				return
			else:
				part = part.replace(":", "") # gets rid of pesky colons interfere with SMS (colons result in blank texts)
				server.sendmail(self._username, self._phone, part) # send message to phone carrier SMS email address
				sentCount += 1

	def start(self):
		""" Starts checking for new important mail """
		while True:
			self.checkMail()
			time.sleep(self._restTime)
