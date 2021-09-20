#!/usr/bin/python3

# Modified version of the geoparser script to accept a single filename and process the contents

from mordecai import Geoparser
import re
import os

xmlfile = re.compile('.*\.xml')
geo = Geoparser()

inputfile = input("Please enter the name of the file you wish to process: ")

if xmlfile.match(inputfile): # Only process XML files
	with open(inputfile, "r") as infile:
		print("Processing data from " + inputfile + "...")
		data = infile.readlines()
	infile.close()

	output = geo.geoparse(str(data))

	name, extension = os.path.splitext(inputfile)
	outfilename = name + "_output.txt"

	with open(outfilename, "a") as outfile:
		for word in output:
			outfile.write(str(word))
			outfile.write("\n")

	outfile.close()
