#!/usr/bin/python3
# Currently modified to process only one file each time the script is run
from mordecai import Geoparser
import re
import os

xmlfile = re.compile('.*\.xml')
#geo = Geoparser()

for inputfile in os.listdir("./processed_files"):
	name, extension = os.path.splitext(inputfile)
	outfilename = name + "_output.txt"
	inputfile = "./processed_files/" + inputfile
	print("Outfile name: "+outfilename)
	if xmlfile.match(inputfile) and outfilename not in os.listdir("./processed_files"): # Only process XML files
		geo = Geoparser()
		with open(inputfile, "r") as infile:
			print("Processing data from " + inputfile + "...")
			data = infile.readlines()
		infile.close()

		output = geo.geoparse(str(data))
		outfilename = "./processed_files/" + outfilename

		with open(outfilename, "a") as outfile:
			for word in output:
				outfile.write(str(word))
				outfile.write("\n")

		outfile.close()
		break
		quit() # End script execution

