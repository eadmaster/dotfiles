#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: read args: $0 site master_pass
# TODO:  reuse https://github.com/SriLikesToSing/fastLane

def pwgen_random(alphabet, length=12):
	import random
	try:
		# using urandom wrapper (safer, no need for seeding)
		temp = random.SystemRandom.sample(alphabet, length)
	except:
		random.seed()
		temp = random.sample(alphabet, length)
	password = "".join(temp)
	return(password)


def pwgen_secrets(alphabet, length=12, min_digits=2):
	# source: https://geekflare.com/password-generator-python-code/
	# req. py > 3.6
	import secrets
	while True:
		pwd = ''
		for i in range(length):
			pwd += ''.join(secrets.choice(alphabet))

		# check constraints: should contain at least 1 special character, should contain at least 2 digits
		if (any(char in special_chars for char in pwd) and sum(char in digits for char in pwd)>=min_digits):
			  break
		# end for
	# end while
	return(pwd)


def pwgen_uuid4(length):
	import uuid
	return(str(uuid.uuid4())[0:length])
	
	
if __name__ == "__main__":
	# define the alphabet
	import string
	letters = string.ascii_letters
	digits = string.digits
	special_chars = string.punctuation
	alphabet = letters + digits + special_chars
	
	# TODO: allow passing max lenght, requirements  https://linux.die.net/man/1/pwgen

	# fixed password length
	pwd_length = 12
	
	try:
		print(pwgen_secrets(alphabet, pwd_length))
	except:
		print(pwgen_random(alphabet, pwd_length))
		#print(pwgen_uuid4(pwd_length))
	