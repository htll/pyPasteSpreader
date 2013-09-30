import urllib
import base64
import json
import sys
from optparse import OptionParser
from time import sleep

#paste.kde.org
class KDE:
	def __init__(self):
		self.url = "http://paste.kde.org/"

	def upload(self,data):
		#First Base64 Encode the data-chunck
		b64_result = base64.b64encode(data,None)

		#Populate dictionary for api
		post = {}
		#Data we wish to post
		post["paste_data"] = b64_result
		#Format of data
		post["paste_lang"] = "text"
		#Private
		post["paste_private"] = "yes"
		#Required by api
		post["api_submit"] = "true"
		#Return format
		post["mode"] = "json"
		#Never expire
		post["paste_expire"] = 0

		#Turn dictionary into key=val string suitable for post
		post_data = urllib.urlencode(post)
		#Open connection to site with post data	and return json data as an object
		response = json.loads(urllib.urlopen(self.url,post_data).read())
		
		#Spam guard check
		if response["result"].has_key("error"):
			#print "Hit the spam guard!!!"
			return "Spamguard_error"

		#Get the paste id
		paste_id = response["result"]["id"]
		#Get the private hash
		paste_hash = response["result"]["hash"]
		#return the url + location of new paste + resulting hash in order to view private posts
		return self.url + paste_id + "/" + paste_hash


#Borrowed from Stackoverflow
def split_str(s, l=2):
    return [s[i:i+l] for i in range(0, len(s), l)]


#Function to actually push the data to the pastebins
def push(opt):
	kde = KDE()
	filename = args[0]
	#If we are outputting to a file
	if opt.output:
		print "Writing to",opt.output
		outfile = open(opt.output,"w")
		outfile.write(filename + "\n")
	#get file data		
	spread = open(filename,"rb").read()
	#get size of file
	spread_size = len(spread)
	#get file chunk size
	part_size = spread_size / int(opt.chunks)
	#split the data into chunks
	parts = split_str(spread,part_size)
	count = 1
	#Iterate over parts
	for part in parts:
		if opt.output:
			#write the url to the file
			outfile.write(kde.upload(part,opt.proxy) + "\n")
		print kde.upload(part)
		sleep(float(opt.sleep_time))
	#close the file		
	if opt.output:
		outfile.close()

#Function to read a file containing the links to the parts of a file
def pull(opt):
	pass
		
if __name__ == "__main__":
	usage = "Usage: %prog [Options] file"
	desc = "Splits a file into chunks, base64 encodes those chunks and uploads them to various pastebins. Original idea from pyCloudForce"
	parser = OptionParser(usage=usage,description=desc)
	parser.add_option("-m","--mode",dest="mode",help="action to use 'push' files/'pull'reconstruct files")
	parser.add_option("-c","--chunks",default=2,dest="chunks",help="How many chunks you wish to split the file into(Default 2)")
	parser.add_option("-o","--output",dest="output",help="Output file that holds the links to your spread data")
	parser.add_option("-s","--sleep",dest="sleep_time",default=3,help="Time to wait before pushing the next chunk(Default 3)")
	(options, args) = parser.parse_args()
	if options.mode == "push":
		push(options)
	elif options.mode == "pull":
		pull(options)
	else:
		parser.print_help()			

