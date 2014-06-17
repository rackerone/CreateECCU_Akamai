#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright 2013 Aaron Smith

#You can enter a space-separated list of container URLs when prompted for input.
#OR, you can save a file named 'purge_urls.txt' in the current working directory that contains a single URL per line as input

import os
import sys

GREETING = "Welcome to the Rackspace ECCU file generator."
URL_LIST_FILE = 'purge_urls.txt'
ECCU_PURGE_FILE = 'purge.data'
#Set up the eccu file template
eccu_txt = """<?xml version="1.0"?>
<eccu>
    <match:request-header operation="name-value-cmp" argument1="Host" argument2="%s">
        <revalidate>now</revalidate>
    </match:request-header>
</eccu>
"""

def clear_screen():
	"""Clear the screen to make output more legible"""
	os.system('cls' if os.name == 'nt' else 'clear')

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
			print "The file '%s' is empty!  Please add URLs to the file or enter them manually." % URL_LIST_FILE
			sys.exit(1)
		#Append all URLs to the list named "my_urls"
		with open(URL_LIST_FILE) as f:
			for line in f.readlines():
				my_urls.append(line)
	except IOError,OSError:
		print "Files '%s' does not exist or is not accessible.  Please verify this files exists and has the correct permissions and try again." % URL_LIST_FILE
		#sys.exit(1)
	#Stripping off any newline characters from the right side of each URL
	my_urls = [url.rstrip() for url in my_urls]
	#Cleaning up the URL list and making a them into a space-separated string
	for url in my_urls:
		input_urls = (input_urls + ' ' + url)
	#Strip off any white space on either end of the string
	input_urls = input_urls.strip()
elif (input_file.lower() == "no" or input_file.lower() == "n"):
	print "You chose to manually input URLs!\n"
	#Here we are manually entering URLs
	input_urls = raw_input("Please enter a single URL, or a list of URLs, each separated by a single space:\n")
	input_urls = input_urls.strip()
else:
	print "Unable to understand answer, assuming you will enter URLs manually.\n"
	#Here we are manually entering URLs
	input_urls = raw_input("Please enter a single URL, or a list of URLs separated by a single space: ")
	input_urls = input_urls.strip()

data = eccu_txt % input_urls

with open(ECCU_PURGE_FILE, 'w') as f:
	f.write(data)
	f.flush()

clear_screen()
print "The following xml data has been added to a file in the current directory named '%s'!\n\n" % ECCU_PURGE_FILE
print data





