# For testing settings.py

import settings as my_settings
from django.conf import settings

settings.configure(my_settings)

import smtplib

fromMy = settings.DEFAULT_FROM_EMAIL
to  = 'chaim.leib.halbert@gmail.com'
subj='Test Python'
date='3/18/2015'
message_text='Hello Or any thing you want to send'

msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromMy, to, subj, date, message_text )

username = settings.EMAIL_HOST_USER
password = settings.EMAIL_HOST_PASSWORD
host = settings.EMAIL_HOST
port = settings.EMAIL_PORT

server = smtplib.SMTP(host, port)
server.starttls()
server.login(username, password)
server.sendmail(fromMy, to, msg)
server.quit()

print("Success")