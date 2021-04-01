#getRawTest.py
#Takes raw files from directories specified manually in this script and sends
#output to a file in another directory keeping only text that 
#follows the regex defined in this script.

import sys
import os
import re
from pathlib import Path

os.chdir('../')

output_folder = 'processed_files'
#First column is the name of the folder where files of this format will be found
#Second column is a list of 2-tuples, they are the begining and end tags for raw text in the format for that folder
input_dirs = [
    ('Geoderma',  [("<xocs:rawtext>","</xocs:rawtext>"),("<dc:description>","</dc:description>")]),
    ('AOUxml',  [("<xocs:rawtext>","</xocs:rawtext>"),("<dc:description>","</dc:description>")]),
#    ('RSE',       [("<xocs:rawtext>","</xocs:rawtext>")]),
#RSE is to big for testing, uncomment later
    ]


#Create directory for output
p = Path(output_folder)
try:
    p.mkdir()
except FileExistsError as exc:
    print(exc)

#Open test files
for folder in input_dirs:
    directory = r'./' + folder[0]
    directory2 = r'./' + output_folder
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            #only do .xml files
            if not filename.endswith(".xml"):
                continue
            with open(root + '/' + filename, 'r',errors='ignore') as file:
                #Check for match
                line = file.read()
                print(filename)
                f = open(directory2 + '/' + folder[0] + filename,"w")
                for tags in folder[1]:
                    result = re.search(tags[0] + '.*' + tags[1],line)

                    #Send output to test file
                    if result:
                        f.write(result.group(0)[len(tags[0]):-len(tags[1])])
                        print('\t' + tags[0] + " found")
                    else:
                        print('\t' + tags[0] + " not found")
                f.close()
