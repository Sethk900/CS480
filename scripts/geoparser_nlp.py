#!/usr/bin/python3
#runs the mordecai geoparser on a set of files
from mordecai import Geoparser
import re
import os

#if true then it will replace the existing ouput files with new ones
redo_articles = False

#these are the input folders and their corresponding output folders 
folders = [
#	("../processed_files/jmap/","../geoparser_output/jmap/")
#	("../processed_files/","../geoparser_output/")	  # Only processing jmap right now
	]
	
#put any individual files you want processed here, you can use this to process a single file
files = [
	("../processed_files/Geoderma10.1016.0016-7061(75)90014-2.xml","../output_test_nlp.txt"),
	("../processed_files/Geoderma10.1016.0016-7061(84)90041-7.xml","../output_test2_nlp.txt")
	#("./vernacular.txt","./vern_output.txt")
]

xmlfile = re.compile('.*\.xml')

# Regular expressions for filters
capital = re.compile('.*[A-Z]*.*')
allLowercase = re.compile('^[a-z]+$')
twoLetter = re.compile('[a-zA-Z][a-zA-Z]$')
specialChars = re.compile('.*[^a-zA-Z ].*')




#after this loop, the files list has all the files that are going to be processed
for inputfolder,outputfolder in folders:
	for inputfile in os.listdir(inputfolder):
		name, extension = os.path.splitext(inputfile)
		outputfile = name + "_output.txt"
		if xmlfile.match(inputfile) and (redo_articles or outputfile not in os.listdir(outputfolder)): # Only process XML files
			files.append((inputfolder + inputfile, outputfolder + outputfile))
			
geo = Geoparser()
speciesFlag = False   #For the species cross-referencing

#opens the input and ouput files and runs the geoparser
for inputfile,outputfile in files: 
	print("Outfile name: "+outputfile)
	with open(inputfile, "r", encoding="utf-8", errors="ignore") as infile:
		print("Processing data from " + inputfile + "...")
		try:
			data = infile.readlines()
		except:
			with open(outputfile, "a") as outfile:
				outfile.write("Unicode Error")
			outfile.close()
			data = "none"
		infile.close()
	with open(outputfile, "a", errors='ignore') as outfile:
		for line in data:
			print("Geoparser start")
			output = geo.geoparse(line)
			print("Geoparser end")
			for place in output:
				'''
				IMPLEMENT FILTERS HERE
				Filters, at least right now, are typically implemented using regular expressions. 
				To implement one, you should build a regular expression that matches an attribute that you want to exclude from the geoparser output. 
				Then, use the if statement below to filter out geonames that possess that attribute.
				'''
                
				if capital.match(place['word']) and not(specialChars.match(place['word']) or allLowercase.match(place['word']) or twoLetter.match(place['word'])): # Filter out place names that don't contain any capital later (Comment out to remove filter)
					try:
						if speciesFlag == False:
							outfile.write(str(place))
							outfile.write("\n")
					except:
						print("Unicode error when trying to write word " + word['word'] + " to outfile.")
				
				speciesFlag = False   #Reset
		outfile.close()
