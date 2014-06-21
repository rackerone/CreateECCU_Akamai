#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright 2014 Aaron Smith

#You can enter a space-separated list of container URLs when prompted for input.
#OR, you can save a file named 'purge_urls.txt' in the current working directory \
#that contains a single URL per line as input

import os
import sys
import subprocess

GREETING = "Welcome to the Rackspace ECCU file generator."
URL_LIST_FILE = 'purge_urls.txt'
COMMAND = 'publisheccu'
ECCU_PURGE_FILE = 'purge.data'
WORKING_DIRECTORY = os.path.expanduser('~/bin/akamai/publisheccu')
AKAMAI_PASSWORD = os.environ["AKAMAI_PASSWORD"]
AKAMAI_USERNAME = os.environ["AKAMAI_USERNAME"]

#Set up the eccu file template.  Our "ECCU_PURGE_FILE" (purge.data), as mentioned \
#above, will contain this information along with the list of URLs to purge as the \
#value to 'argument2'.
purge_Data = """<?xml version="1.0"?>
<eccu>
    <match:request-header operation="name-value-cmp" argument1="Host" argument2="%s">
        <revalidate>now</revalidate>
    </match:request-header>
</eccu>"""

#The properties file is used to set some metadata about the transaction.  We will set the filename \
#email address of the executor of the script, etc.  Thsi is a MANDATORY file, as it holds the \
#information that would have been filled out in the Akamai control panel about this purge.
properties_Data = """filename=Testing Publish_eccu         <=====this line does not actually set filename for some reason
notes=I am simply testing web services here       <====-use the 'notes' line for title and note info
version=3.0
propertyName=cf1.rackcdn.com
propertyType=hostheader
propertyNameExactMatch=false
statusChangeEmail=aaron.smith@rackspace.com"""

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

clear_screen()
print ('-' * len(GREETING))
print GREETING
print ('-' * len(GREETING))
print '\n\n'


#Here we are determining if this script should use an input file containing URLs to purge, or if we are entering URLs manually.
input_file = raw_input("Do you have a '%s' file in the current working directory containing a list of URLs you would like purged? [Yes|No] " % URL_LIST_FILE)

if (input_file.lower() == "yes" or input_file.lower() == "y"):
	print "You are using the following file as input for this script: %s" % URL_LIST_FILE
	#Add each URL in the file to this list
	my_urls = []
	try:
		#Checking to see if file is 0-byte length (empty) and if so exiting
		if (os.stat(URL_LIST_FILE)[6] == 0):
			sys.exit("The file '%s' is empty!  Please add URLs to the file or enter them manually." % URL_LIST_FILE)
		#Append all URLs to the list named "my_urls"
		with open(URL_LIST_FILE) as f:
			for line in f.readlines():
				my_urls.append(line)
	except IOError,OSError:
		sys.exit("Files '%s' does not exist or is not accessible.  Please verify this files exists and has the correct permissions and try again." % URL_LIST_FILE)
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
else:
	clear_screen()
	print "Unable to understand answer, assuming you will enter URLs manually.\n"
	#Here we are manually entering URLs
	input_urls = raw_input("Please enter a single URL, or a list of URLs separated by a single space: ")
	input_urls = input_urls.strip()

if (len(input_urls) > 400):
	clear_screen()
	sys.exit("ERROR!  You have more than 400 container URLs in a single ECCU file (purge.data).  Please trim the number of URLs down to chunks of 400 and retry!")

data = purge_Data % input_urls

with open(ECCU_PURGE_FILE, 'w') as f:
	f.write(data)
	f.flush()

clear_screen()

#Get the current where this script is being executed from.  We are \
#going to save the eccu 'purge.data' file there.
execution_Dir = os.path.dirname(os.path.abspath(__file__))
#Create an exit messge
EXIT_MESSAGE = "The following xml data has been added to this file: '%s" % execution_Dir + '/' + ECCU_PURGE_FILE + "'\n"
print "%s\n" % EXIT_MESSAGE
print "FILENAME: %s" % ECCU_PURGE_FILE
print (('-' * len(EXIT_MESSAGE)) + '\n')
print data
print ('\n' + ('-' * len(EXIT_MESSAGE)))


#Notes
#get current directory that this script is being executed from
#  os.path.dirname(os.path.abspath(__file__))

