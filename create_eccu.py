#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright 2014 Aaron Smith

#You can enter a space-separated list of container URLs when prompted for input.
#OR, you can save a file named 'purge_urls.txt' in the current working directory \
#that contains a single URL per line as input.  When asked if you have a list of \
#URLs to supply from a file, say yes.

import os
import sys
import subprocess
#import traceback

GREETING = "Welcome to the Rackspace ECCU file generator."
URL_LIST_FILE = 'purge_urls.txt'
COMMAND = 'publisheccu'
ECCU_PURGE_FILE = 'purge.data'
WORKING_DIRECTORY = os.path.expanduser('~/bin/akamai/publisheccu')
#Get the current directory where this script is being executed from.  We are \
#going to save the eccu 'purge.data' file there.  Where ever whe are, purge.data \
#is dropped directly into our local directory that contains this script.
EXECUTION_DIR = os.path.dirname(os.path.abspath(__file__))


#Set up the eccu file template.  Our "ECCU_PURGE_FILE" (purge.data), as mentioned \
#above, will contain this information along with the list of URLs to purge as the \
#value to 'argument2'.
PURGE_DATA = """<?xml version="1.0"?>
<eccu>
    <match:request-header operation="name-value-cmp" argument1="Host" argument2="%s">
        <revalidate>now</revalidate>
    </match:request-header>
</eccu>"""

#The properties file is used to set some metadata about the transaction.  We will set the filename \
#email address of the executor of the script, etc.  This is a MANDATORY file, as it holds the \
#information that would have been filled out in the Akamai control panel about this purge.
#Of Note:
#  -The "filename" property does not seem to actually set a filename.  The "notes" property however does \
#    actually work.  So we will get a "filename" from the user and set that value for the "filename" and \
#    "note" properties.  The "note" property will essentially be the filename.
#  -The "propertyName" property will be

PROPERTIES_DATA = """filename={filename}
notes={notes}
version=3.0
propertyName=cf1.rackcdn.com
propertyType=hostheader
propertyNameExactMatch=false
statusChangeEmail=user@example.com"""

def clear_screen():
	"""Clear the screen to make output more legible"""
	os.system('cls' if os.name == 'nt' else 'clear')

def PublishECCU(action):
	"""Function used to execute a subprocess call.  We will be calling the 'publichECCU.sh' Akamai SOAP client (java based)"""
	actions_list = ['list', 'delete', 'upload', 'get_info', 'edit_notes', 'edit_email']
	if action not in actions_list:
		clear_screen()
		print "ERROR!  The 'action' command supplied to the 'purge_URLs' function does not exist.  See Below!\n"
		sys.exit(subprocess.call(COMMAND))
	##This is the subprocess call that will work properly.  Using "shell=True" usually is not a good idea but it makes this work easily.
	##I am not relying on user input for the variables in this command anyway.  I am also redirecting stderr to stdout.
	#subprocess.check_call('publisheccu %s %s list' % (AKAMAI_USERNAME, AKAMAI_PASSWORD), shell=True, cwd=WORKING_DIRECTORY, stderr=subprocess.STDOUT)

#Initialize variable.  This will be the final list of URLs that will be supplied to the eccu file as a space separated list
input_urls = ''

#wrapping this entire script in a try/except to catch a control-c to get out of it without puking a stacktrace
try:
	#Set up greeting upon script launch
	clear_screen()
	print ('-' * len(GREETING))
	print GREETING
	print ('-' * len(GREETING))
	print '\n'

	#Attempt to retrieve credentials from environment variables.  If not present, manually add them for \
	#the current runtime environment.
	try:
		AKAMAI_USERNAME = os.environ["AKAMAI_USERNAME"]
	except KeyError:
		print "ERROR!  Unable to find 'AKAMAI_USERNAME' in user environment variables!"
		username = raw_input("	====>Please set 'AKAMAI_USERNAME' environment variable.\n\nFor now, manually enter your AKAMAI_USERNAME: ")
		os.environ['AKAMAI_USERNAME'] = username
		AKAMAI_USERNAME = os.environ["AKAMAI_USERNAME"]
		clear_screen()
		print "Environment variable 'AKAMAI_USERNAME' has been set to: %s\n" % username
	try:
		AKAMAI_USERNAME = os.environ["AKAMAI_PASSWORD"]
	except KeyError:
		print "Unable to find 'AKAMAI_PASSWORD' in user environment variables!"
		passwd = raw_input("	====>Please set 'AKAMAI_PASSWORD' environment variable.\n\nFor now, manually enter your AKAMAI_PASSWORD: ")
		if (len(passwd) > 0):
			clear_screen()
			print "Your 'AKAMAI_PASSWORD' for this script run has been set.  For security purposes it will not be printed to screen."
		else:
			sys.exit("ERROR!  You must supply a password to this script OR set the appropriate environment variable [AKAMAI_USERNAME].")
		os.environ['AKAMAI_PASSWORD'] = passwd
		AKAMAI_USERNAME = os.environ["AKAMAI_PASSWORD"]

	#Here we are determining if this script should use an input file containing URLs to purge, or if we are entering URLs manually.
	input_file = raw_input("Do you have a '%s' file in the current working directory containing a list of URLs you would like purged? [Yes|No] " % URL_LIST_FILE)

	if (input_file.lower() == "yes" or input_file.lower() == "y"):
		print "You are using the following file as input for this script: %s" % URL_LIST_FILE
		#Add each URL in the file to this list
		my_urls = []
		try:
			#Checking to see if file is 0-byte length (empty) and if so exiting
			if (os.stat(URL_LIST_FILE)[6] == 0):
				sys.exit("The file '%s' is empty!  Please add URLs (one per line) to the file or enter them manually." % URL_LIST_FILE)
			#Append all URLs to the list named "my_urls"
			with open(URL_LIST_FILE) as f:
				for line in f.readlines():
					my_urls.append(line)
		except (IOError,OSError) as e:
			#sys.exit("File '%s' does not exist or is not accessible.  Please verify this files exists and has the correct permissions and try again." % URL_LIST_FILE)
			clear_screen()
			print "ERROR!"
			print "File '%s' does not exist or is not accessible.  Please verify this files exists and has the correct permissions and try again.\n" % URL_LIST_FILE
			sys.exit(1)
		#Stripping off any newline characters from the right side of each URL
		my_urls = [url.rstrip() for url in my_urls]
		#Cleaning up the URL list and making a them into a space-separated string
		for url in my_urls:
			input_urls = (input_urls + ' ' + url)
		#Strip off any white space on either end of the string
		input_urls = input_urls.strip()
	elif (input_file.lower() == "no" or input_file.lower() == "n"):
		clear_screen()
		print "You chose to manually input URLs!\n"
		#Here we are manually entering URLs
		input_urls = raw_input("Please enter a single URL, or a list of URLs, each separated by a single space:\n")
		input_urls = input_urls.strip()
		if (len(input_urls) > 1):
			clear_screen()
			print "Your URL(s) have been set and will be supplied as 'argument2' in the eccu file."
		else:
			clear_screen()
			print "ERROR!"
			print "You must not have entered any URLs because the 'input_url' list is empty.  Rememeber to supply a space-separated list when asked.\n"
			sys.exit(1)
	else:
		clear_screen()
		print "Entering default mode.  Assuming you will enter URLs manually.\n"
		#Here we are manually entering URLs
		input_urls = raw_input("Please enter a single URL, or a list of URLs separated by a single space: \n")
		input_urls = input_urls.strip()

	if (len(input_urls.split(' ')) > 400):
		clear_screen()
		sys.exit("ERROR!  You have more than 400 container URLs in a single ECCU file (purge.data).  Please trim the number of URLs down to chunks of 400 and retry!")

	data = PURGE_DATA % input_urls

	#Create the purge.data file
	with open(ECCU_PURGE_FILE, 'w') as f:
		f.write(data)
		f.flush()

	clear_screen()

	#Create an exit messge
	EXIT_MESSAGE = "The following xml data has been added to this file: '%s" % EXECUTION_DIR + '/' + ECCU_PURGE_FILE + "'\n"
	print "%s\n" % EXIT_MESSAGE
	print "FILENAME: %s" % ECCU_PURGE_FILE
	print (('-' * len(EXIT_MESSAGE)) + '\n')
	print data
	print ('\n' + ('-' * len(EXIT_MESSAGE)))
except KeyboardInterrupt as e:
	clear_screen()
	print "Canceling all the things!\nThank you, come again!\n"

