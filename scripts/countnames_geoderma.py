#!/usr/bin/python3
# This script iterates through geoparser output and determines which place name is mentioned the most times

import json, ast, os, re

geoderma = re.compile('.*Geoderma.*')

#infile = input("Enter the name of a file you'd like to analyze: ")
#infile = "../geoparser_output/" + infile
outfile = "countnames_output.txt"

checked_names = []

#max_count = 0
#top_name = ""
#second_name = ""

output = open(outfile, "w");

for file in os.listdir("/JournalMap/CS480/geoparser_output/"):
	infile = "../geoparser_output/" + file
	max_count = 0
	top_name = ""
	second_name = ""
	if(geoderma.match(file)==None):
		continue
	with open(infile, "r") as input:
		try:
			lines = input.readlines()
		except:
			continue
		for line in lines:
#			print(line)
			try:
				word = ast.literal_eval(line)
			except:
				continue
			placename = word['word']
			if placename not in checked_names:
				count = 0
				checked_names.append(placename)
				test = open(infile, "r")
				for line1 in test.readlines():
					try:
						checkword = ast.literal_eval(line1)
					except:
						continue
					if checkword['word'] == placename:
						count = count + 1
				if count > max_count:
					max_count = count
					second_name = top_name
					top_name = placename
				# Count the number of times that the name was referenced in the file
			else:
				continue

		input.close()
	if max_count > 0:
		output.write("FILE: " + str(file) + " TOP NAME: "+ top_name + " (appears " + str(max_count) + " times)" + " SECOND NAME: " + second_name)
		output.write("\n")

output.close()
