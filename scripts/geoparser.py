#!/usr/bin/python3
from mordecai import Geoparser
import re
import os

xmlfile = re.compile('.*\.xml')
geo = Geoparser()

for inputfile in os.listdir("./processed_files"):
	if xmlfile.match(inputfile): # Only process XML files
		inputfile = "./processed_files/" + inputfile
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
