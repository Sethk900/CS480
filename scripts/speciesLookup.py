#This is a function that will accept a string and key, and it will search that string 
#for a species name.  It will return true or false.
#Usage: speciesLookup(inputString,lookup_key) ---> True/False

import json

lookup_file = open("lookupDict.json", "r",errors="ignore")   #Open the lookup file for string analysis
lookup_dictionary = json.load(lookup_file)                   #The actual lookup dictionary
lookup_file.close()

def speciesLookup(inputString,lookup_key):
    '''UNCOMMENT for debug'''
    #print("Check " + lookup_key + " in lookup dictionary and evaluate '" + inputString + "'\n")

    #Run analysis
    try:
        for name in lookup_dictionary[lookup_key]:
            if(name in inputString):
                return True   #We FOUND a species name
    except:
        print("Key error... " + lookup_key + " does not seem to exist within the lookup dictionary.\n")

    return False          #We did NOT FIND a species name
    