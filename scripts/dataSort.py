#Python 3 program for taking a data set from the vernaculars.txt file and sorting it
# into a new output.txt file that will simply contain the alphabetical list of proper names.
# This script directly interacts with crossSearch.py.

from mordecai import Geoparser
import os

geo = Geoparser()

#Open vernaculars.txt file (the database of names)
namesFile = open("vernaculars.txt", "r")

presortArray = []   #Will contain the data from the file before sorting it
flag = False        #Will determine if we add the current character to the working string

for line in namesFile:
    workingString = ""   #Resets the working string
    for character in line:
        if(flag == True and character != '|'):
            workingString = workingString + character
        if(character == '|' and flag == True):
            flag = False
            break
        if(character == '|' and flag == False):
            flag = True
    parse = geo.geoparse(workingString)
    #Check to see if it's a place name.  If true, add it.  Otherwise, ignore.
    if (len(str(parse)) > 0):
        word = parse['word']                        #Take the literal match from mordecai
        presortArray.append((word,workingString))   #Add the entry to the array with our full species name

namesFile.close()          #Close the vernaculars file
presortArray.sort()        #Sort the array of names

with open("output.txt", "w") as outputFile:
    for line in presortArray:
        outputFile.write("".join(line) + "\n") # works with any number of elements in a line

outputFile.close()   #Close the output file
