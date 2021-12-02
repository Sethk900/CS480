#!/usr/bin/python3
#runs the mordecai geoparser on a set of files
from mordecai import Geoparser
import re
import os

import spacy
nlp=spacy.load('en_core_web_sm')

#Species crossreferencing function
from speciesLookup import *

#if true then it will replace the existing ouput files with new ones
redo_articles = True

#these are the input folders and their corresponding output folders 
folders = [
	("../processed_files/jmap/","../geoparser_output/jmap/"),
	("../processed_files/","../geoparser_output/")	  # Only processing jmap right now
	]
	
#put any individual files you want processed here, you can use this to process a single file
files = [
	#("../processed_files/Geoderma10.1016.0016-7061(75)90014-2.xml","../output_test.txt"),	  
	#("../processed_files/Geoderma10.1016.0016-7061(84)90041-7.xml","../output_test2.txt"),
	#("../tests/test_input.txt","../tests/test_output.txt")
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

#function used by the spacy processing
def get_objects(tree,object_types):
	objects = []
	for child in tree.children:
		flag = True
		for object_type in object_types:
			if(object_type in child.dep_):
				objects+=[''.join([token.text_with_ws for token in list(child.subtree)]).strip()]
				flag = False
		if(flag):
			objects+=get_objects(child,object_types)
	return objects

total_files = len(files)
current_file = 0

#opens the input and ouput files and runs the geoparser
for inputfile,outputfile in files:
	current_file += 1
	print("Processing file",current_file,"out of", total_files)
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
		#print("Spacy processing start")
		parsed_doc = nlp(''.join(data))
		place_strings = []
		for token in parsed_doc:
			if(token.dep_ == 'ROOT'):
				sentence = ''.join([token2.text_with_ws for token2 in list(token.subtree)]).strip()
				for obj in get_objects(token,['subj', 'obj']):
					if(len(nlp(obj).ents) != 0):
						place_strings += [(obj,sentence)]
		#print("Spacy processing end")
		#print("Geoparser start")
		output = []
		for string in place_strings:
			places = geo.geoparse(string[0])
			for place in places:
				place['phrase'] = string[0]
				place['sentence'] = string[1]
			output += places
		#print("Geoparser end")
		for place in output:
			'''
			IMPLEMENT FILTERS HERE
			Filters, at least right now, are typically implemented using regular expressions. 
			To implement one, you should build a regular expression that matches an attribute that you want to exclude from the geoparser output. 
			Then, use the if statement below to filter out geonames that possess that attribute.
			'''
			#Initialize or Reset filters
			speciesFlag = False
			capitalFlag = False	

			# Perform species list crossreferencing (comment out to remove filter)
			if speciesLookup(place['phrase'],place['word']) == True:
				speciesFlag = True	 #Species name found
				#print("Species Flag triggered on " + place['word'] + "\n")

			# Filter out place names that don't contain any capital later (Comment out to remove filter)
			if capital.match(place['word']) and not(specialChars.match(place['word']) or allLowercase.match(place['word']) or twoLetter.match(place['word'])):
				capitalFlag = False	  #Do nothing, no unusual input
			else:
				capitalFlag = True	  #Capital issue found
				#print("Capital Flag triggered on " + place['word'] + "\n")
			
			#Write to output file if all flags are false
			if speciesFlag == False and capitalFlag == False:
				try:
					outfile.write(str(place))
					outfile.write("\n")	
				except:
					print("Unicode error when trying to write word " + word['word'] + " to outfile.")	
		outfile.close()
