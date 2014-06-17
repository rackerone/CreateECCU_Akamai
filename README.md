CreateECCU_Akamai
=================

Create an ECCU file for Akamai purge requests

For now, simply execute this at the command line and follow instructions.  

$ python create_eccu.py

You can enter a space-separated list of container URLs to purge, or you can supply a file that contains one container URL per line.

If you are supplying a list of container URLs by file, then create a file named "purge_urls.txt" in the current working directory of this script.  Again, one container URL per line.

Once this script is done, it will print the 'contents' of the ECCU xml file to the screen, but it will also create the actual ECCU file in the current working directory.  The name of this file will be "purge.data".

Now you can log into the Akamai control panel and supply this "purge.data" file as the ECCU file to purge.  

I am working on extending the functionality of this script to actually handle the purges as well.  This will require a service account on a server and will only be accessible by a few people because it will have credentials coded into it.  

NOTE:  I have limited the number of actual container URLs to 400 for a single run of this script.  I have found that this number of URLs will complete successfully.  The reason for this is that there is a 32K max file size for the "purge.data" file.  Also, we NEVER want more than 10,000 outstanding requests queued for our (rackspace) account at once because it could trigger an entire account purge.
