#!/usr/bin/env python3

# derived from  https://www.geeksforgeeks.org/fetch-unseen-emails-from-gmail-inbox/

import imaplib
import email
from email.header import decode_header
import webbrowser
import os
 
username = os.getenv("GMAIL_USERNAME") + '@gmail.com'
password = os.getenv('GMAIL_APP_PASSWORD')

imap = imaplib.IMAP4_SSL("imap.gmail.com")
  
result = imap.login(username, password)
  
imap.select('Inbox', readonly = True) 
  
response, messages = imap.search(None, 'UnSeen')
messages = messages[0].split()
  
# take it from last
latest = int(messages[-1])
  
# take it from start
oldest = int(messages[0])

#max_subj_len = os.get_terminal_size().columns - 40
max_subj_len = 40

for i in range(latest, latest-20, -1):
	# fetch
	res, msg = imap.fetch(str(i), "(RFC822)")
	  
	for response in msg:
		if not isinstance(response, tuple):
			continue
		msg = email.message_from_bytes(response[1])
		# try to match mailx format http://linux.math.tifr.res.in/linux-manual/mailx.jpg
		from_str = msg["From"]
		date_str = msg["Date"]
		from_formatted = from_str.split()[-1].strip("<>")
		date_formatted = email.utils.parsedate_to_datetime(date_str).strftime('%a %b %d %H:%M')
		subject_formatted = msg["Subject"][:max_subj_len]
		print(" %3.3d %16.16s  %s  %s" % (i, from_formatted, date_formatted, subject_formatted))
		## TODO: add url to view the mail in the browser?

	#for part in msg.walk():
	#    if part.get_content_type() == "text / plain":
	#        # get text or plain data
	#        body = part.get_payload(decode = True)
	#        print(f'Body: {body.decode("UTF-8")}', )