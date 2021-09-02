#!/usr/bin/python3
# This script iterates through geoparser output and determines which place name is mentioned the most times

import json, ast

infile = input("Enter the name of a file you'd like to analyze: ")
infile = "../geoparser_output/" + infile

checked_names = []

max_count = 0
top_name = ""

with open(infile, "r") as input:
	for line in input.readlines():
		word = ast.literal_eval(line)
		placename = word['word']
		if placename not in checked_names:
			count = 0
			checked_names.append(placename)
			test = open(infile, "r")
			for line1 in test.readlines():
				checkword = ast.literal_eval(line1)
				if checkword['word'] == placename:
					count = count + 1
			if count > max_count:
				max_count = count
				top_name = placename
			# Count the number of times that the name was referenced in the file
		else:
			continue

input.close()
print("The most prominent place name in this file is " + top_name + ", which appears " + str(max_count) + " times.")
