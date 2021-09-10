#!/usr/bin/python3
# Currently modified to process only one file each time the script is run
from mordecai import Geoparser
import re
import os

xmlfile = re.compile('.*\.xml')
capital = re.compile('.*[A-Z]*.*')
geo = Geoparser()

for inputfile in os.listdir("../processed_files/jmap"): # Only processing jmap right now
	name, extension = os.path.splitext(inputfile)
	outfilename = name + "_output.txt"
	inputfile = "../processed_files/jmap/" + inputfile
	print("Outfile name: "+outfilename)
	if xmlfile.match(inputfile) and outfilename not in os.listdir("../geoparser_output/jmap"): # Only process XML files
		#geo = Geoparser()
		with open(inputfile, "r", encoding="utf-8") as infile:
			print("Processing data from " + inputfile + "...")
			try:
				data = infile.readlines()
			except:
				outfilename = "../geoparser_output/" + outfilename
				with open(outfilename, "a") as outfile:
					outfile.write("Unicode Error")
				outfile.close()
				data = "none"
		infile.close()
		outfilename = "../geoparser_output/" + outfilename
		for line in data:
			for word in line.split(): # For testing: eventually we'll want to parse a single word at a time to see what the geoparser is having a hard time with
				#print(word)
				#print("Running geoparser on " + word + "...")
				output = geo.geoparse(str(word))

				#print("Writing geoparser results for to " + outfilename + "...")
				with open(outfilename, "a", errors='ignore') as outfile:
					for line in output:

						'''
						IMPLEMENT FILTERS HERE
						Filters, at least right now, are typically implemented using regular expressions. 
						To implement one, you should build a regular expression that matches an attribute that you want to exclude from the geoparser output. 
						Then, use the if statement below to filter out geonames that possess that attribute.
						'''
						if capital.match(line['word']): # Filter out place names that don't contain any capital later (Comment out to remove filter)
							try:
								outfile.write(str(line))
								outfile.write("\n")
							except:
								print("Unicode error when trying to write word " + word['word'] + " to outfile.")

				outfile.close()
#		break # Temporary modification: process only one file at a time
#		quit() # End script execution
