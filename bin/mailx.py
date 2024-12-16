#!/usr/bin/env python3

# derived from  https://www.geeksforgeeks.org/fetch-unseen-emails-from-gmail-inbox/

import imaplib
import email
import webbrowser
import os
import sys
 
username = os.getenv("GMAIL_USERNAME") + '@gmail.com'
password = os.getenv('GMAIL_APP_PASSWORD')

imap = imaplib.IMAP4_SSL("imap.gmail.com")
  
result = imap.login(username, password)
  
imap.select('Inbox', readonly = True) 


def email_header_to_str(t):
	from email.header import decode_header
	subject_decoded, subject_charset = decode_header(t)[0]
	subject_str = subject_decoded
	if subject_charset:
		subject_str = subject_decoded.decode(subject_charset)
	elif type(subject_decoded) == bytes:
		subject_str = subject_decoded.decode('utf-8')
	return(subject_str)

	
# check args
if len(sys.argv) > 1:
	# feat a single email
	i = sys.argv[1]
	res, msg = imap.fetch(str(i), "(RFC822)")
	for response in msg:
		if isinstance(response, tuple):
			msg = email.message_from_bytes(response[1])
			for item in msg.items():
				print("%s: %s" % (item[0], email_header_to_str(item[1])) )
			#print(msg["Date"])
			#print(msg["From"])
			#print(msg["Subject"])
			
			#from email.parser import HeaderParser
			#h = HeaderParser().parsestr(response[1])
			#print(h.keys())			
	for part in msg.walk():
		if part.get_content_type() == "text/plain":
			# get text or plain data
			body = part.get_payload(decode = True)
			print("") # empty line
			print(body.decode("UTF-8"))
	# TODO: html parser
	exit(0)


#response, messages = imap.search(None, 'UnSeen')
response, messages = imap.search(None, "ALL")
messages = messages[0].split()
  
# take it from last
latest = int(messages[-1])
  
# take it from start
oldest = int(messages[0])

#max_subj_len = os.get_terminal_size().columns - 40
max_subj_len = 60

for i in range(latest, latest-20, -1):

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
		#subject_formatted = msg["Subject"].replace("=?UTF-8?Q?", "")[:max_subj_len]
		# proper subject decoding https://stackoverflow.com/questions/7331351/python-email-header-decoding-utf-8
		subject_formatted = email_header_to_str(msg['subject'])[:max_subj_len]
		print(" %3.3d %16.16s  %s  %s" % (i, from_formatted, date_formatted, subject_formatted))
		## TODO: add an url to view the mail in the browser?

