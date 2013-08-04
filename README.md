Email_SMS_Notifier
==================

A class to check for important Gmail emails and send SMS notification with the sender and message.

Example use:

notifier = Email_SMS_Notifier(yourGmailUsername, yourGmailPassword, 60, 3, yourSMSAddress)
notifier.start()
