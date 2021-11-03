#Python 3 script that will determine the success of the Json solution for
#the place/species name problem.

from mordecai import Geoparser
import os
import json

geo = Geoparser()

#Load the lookup dictionary from the json file
lookup_file = open("lookupDict.json", "r",errors="ignore")
vern_file = open("vernaculars.txt","r",errors="ignore")
output_file = open("proofOutput.txt", "w")
lookup_dictionary = json.load(lookup_file)

total_names = 0
line_count = 0
flag = False

#Move through the file iteratively for each species name
for line in vern_file:
    workingString = ""   #Resets the working string
    for character in line:
        if(flag == True and character != '|'):
            workingString = workingString + character
        if(character == '|' and flag == True):
            flag = False
            break
        if(character == '|' and flag == False):
            flag = True
    #Check to see if it's a place name.
    parse = geo.geoparse(workingString)
    #If true, perform the dictionary lookup.
    for word in parse:
        for name in lookup_dictionary[word['word']]:
            if(name != workingString):                      #If the lookup dict doesn't have it
                output_file.write(workingString + "\n")     #Write to output and tell us what we missed
                total_names = total_names+1                 #Then add to our total names found for final reporting
    line_count += 1
    print(line_count)

#We're done going through the vern file, so conclude results
if(total_names > 0):
    output_file.write("INCOMPLETE: " + str(total_names) + " names were found out of 133,287 total entries.\n")
    print("INCOMPLETE: " + str(total_names) + " names were found out of 133,287 total entries.\n")
else:
    output_file.write("No names found.  We have complete confidence in this filter!\n")
    print("No names found.  We have complete confidence in this filter!\n")

#Close all files
lookup_file.close()
vern_file.close()
output_file.close()
