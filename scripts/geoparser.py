#!/usr/bin/python3
# Currently modified to process only one file each time the script is run
from mordecai import Geoparser
import re
import os

xmlfile = re.compile('.*\.xml')
capital = re.compile('.*[A-Z]*.*')
#geo = Geoparser()

for inputfile in os.listdir("../processed_files"):
	name, extension = os.path.splitext(inputfile)
	outfilename = name + "_output.txt"
	inputfile = "../processed_files/" + inputfile
	print("Outfile name: "+outfilename)
	if xmlfile.match(inputfile) and outfilename not in os.listdir("../geoparser_output"): # Only process XML files
		geo = Geoparser()
		with open(inputfile, "r") as infile:
			print("Processing data from " + inputfile + "...")
			data = infile.readlines()
		infile.close()

		output = geo.geoparse(str(data))
		outfilename = "../geoparser_output/" + outfilename

		with open(outfilename, "a") as outfile:
			for word in output:
				if capital.match(word): # Filter out place names that don't contain any capital later (Comment out to remove filter)
					outfile.write(str(word))
					outfile.write("\n")

		outfile.close()
		break # Temporary modification: process only one file at a time
		quit() # End script execution

