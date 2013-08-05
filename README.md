Email_SMS_Notifier
==================

A class to check for important Gmail emails and send SMS notification with the sender, subject, and message. Built for those without access to a smartphone who don't want to miss out on potentially important emails. While Gmail itself provides the option to do something similar, SMS messages sent from Gmail are limited to 160 characters. The Email_SMS_Notifier class on the other hand will send longer messages in multiple 160 character parts (up to the number of texts you specify for the maximum). Also, this class will only send text notifications for emails Gmail classifies as "important". 

Example Use
=================

notifier = Email_SMS_Notifier(yourGmailUsername, yourGmailPassword, 60, 3, yourSMSAddress)

notifier.start()
