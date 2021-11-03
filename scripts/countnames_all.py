#!/usr/bin/python3
# This script iterates through geoparser output and determines which place name is mentioned the most times

import json, ast, os, re

geoderma = re.compile('.*Geoderma.*')

AOU = re.compile('.*AOU.*')

#if filters is not empty then the script only processes files that pass a filter
filters = [
#	geoderma,
#	AOU
]

#checkes all files in these folders
folders = [
	"/JournalMap/CS480/geoparser_output/",
	"/JournalMap/CS480/geoparser_output/jmap/"
]


#use this if you want to check single files
files = [
#	"/JournalMap/CS480/geoparser_output/singlefile.txt"
]

outfile = "../tests/countnames_output.txt"

output = open(outfile, "w", errors='ignore');

data_dict = {}

#after this loop, the files list has all the files that are going to be processed
for inputfolder in folders:
	for inputfile in os.listdir(inputfolder):
		if(os.path.isdir(inputfile)):
			continue
		if(filters):
			for filtr in filters:
				if(filtr.match(inputfile)==None):
					continue
				else:
					files.append(inputfolder + inputfile)
					break
		else:
			files.append(inputfolder + inputfile)

#counts up the number of times each word is found
for file in files:
	checked_names = {}
	
	try:
		with open(file, "r") as Finput:
			lines = Finput.readlines()
	except:
		continue
	for line in lines:
#		print(line)
		try:
			word = ast.literal_eval(line)
		except:
			continue
		placename = word['word']
		if 'geo' not in word:
			continue
		if placename not in checked_names:
			checked_names[placename] = word['geo']
			checked_names[placename]['count'] = 1
		else:
			checked_names[placename]['count'] = checked_names[placename]['count'] + 1
			
	if(checked_names):
		data_dict[str(file)]=checked_names
		#top_name = max(checked_names, key=checked_names.get)
		#max_count = checked_names[top_name]
		#checked_names[top_name] = 0
		#second_name = max(checked_names, key=checked_names.get)
		#output.write("FILE: " + str(file) + " TOP NAME: "+ top_name + "(appears " + str(max_count) + " times)" + " SECOND NAME: " + second_name)
		#output.write("\n")
	Finput.close()

json.dump(data_dict, output, indent='	 ')

output.close()
