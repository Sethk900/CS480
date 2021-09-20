#!/usr/bin/python3
# Hey Seth, I changed this a lot, let me know if you don't like it, I left the old version at geoparser_old.py
from mordecai import Geoparser
import re
import os

#these are the input folders and their corresponding output folders 
folders = [
	("../processed_files/jmap","../geoparser_output/jmap")
#    ("../processed_files","../geoparser_output")   # Only processing jmap right now
	]
	
#put any individual files you want processed here, you can use this to process a single file
files = [
#    ("../processed_files/singlefile.xml","../geoparser_output/singlefile_output.txt")
]

xmlfile = re.compile('.*\.xml')

# Regular expressions for filters
capital = re.compile('.*[A-Z]*.*')
allLowercase = re.compile('^[a-z]+$')
twoLetter = re.compile('[a-zA-Z][a-zA-Z]$')
specialChars = re.compile('.*[^a-zA-Z ].*')

geo = Geoparser()

#after this loop, the files list has all the files that are going to be processed
for inputfolder,outputfolder in folders:
	for inputfile in os.listdir(inputfolder):
		name, extension = os.path.splitext(inputfile)
		outputfile = name + "_output.txt"
		if xmlfile.match(inputfile) and outfilename not in os.listdir(outputfolder): # Only process XML files
			files.append((inputfolder + inputfile, outputfolder + outputfile))

#this is the same as the old file but without the name processing done by the above loop
for inputfile,outputfile in files: 
	print("Outfile name: "+outputfile)
	with open(inputfile, "r", encoding="utf-8") as infile:
		print("Processing data from " + inputfile + "...")
		try:
			data = infile.readlines()
		except:
			with open(outputfile, "a") as outfile:
				outfile.write("Unicode Error")
			outfile.close()
			data = "none"
	infile.close()
	for line in data:
		for word in line.split(): # For testing: eventually we'll want to parse a single word at a time to see what the geoparser is having a hard time with
			#print(word)
			#print("Running geoparser on " + word + "...")
			output = geo.geoparse(str(word))
			#print("Writing geoparser results for to " + outfilename + "...")
			with open(outputfile, "a", errors='ignore') as outfile:
				for line in output:
					'''
					IMPLEMENT FILTERS HERE
					Filters, at least right now, are typically implemented using regular expressions. 
					To implement one, you should build a regular expression that matches an attribute that you want to exclude from the geoparser output. 
					Then, use the if statement below to filter out geonames that possess that attribute.
					'''
					if capital.match(line['word']) and not(specialCharacters.match(line['word']) or allLowercase.match(line['word']) or twoLetter.match(line['word'])): # Filter out place names that don't contain any capital later (Comment out to remove filter)
						try:
							outfile.write(str(line))
							outfile.write("\n")
						except:
							print("Unicode error when trying to write word " + word['word'] + " to outfile.")

			outfile.close()
