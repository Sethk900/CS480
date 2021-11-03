#!/usr/bin/python3
# Currently modified to process only one file each time the script is run
from mordecai import Geoparser
import re
import os

xmlfile = re.compile('.*\.xml')

# Regular expressions for filters
capital = re.compile('.*[A-Z]*.*')
allLowercase = re.compile('^[a-z]+$')
twoLetter = re.compile('[a-zA-Z][a-zA-Z]$')
specialChars = re.compile('.*[^a-zA-Z ].*')

geo = Geoparser()

for inputfile in os.listdir("../processed_files"):
	inputfile = "../processed_files/" + inputfile
	with open(inputfile, "r", encoding="utf-8") as infile:
		print("Processing data from " + inputfile + "...")
		try:
			data = infile.readlines()
		except:
			print("WARNING: Couldn't read data from file " + str(inputfile))
	infile.close()
	for line in data:
		for word in line.split(): # For testing: eventually we'll want to parse a single word at a time to see what the geoparser is having a hard time with
			try:
				output = geo.geoparse(str(word))
			except:
				print("FOUND A GEOPARSER ERROR")
