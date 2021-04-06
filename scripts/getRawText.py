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
    ('AOUxml',  [("<article-title>","</article-title>"),("<p>","</p>")]),
    ('Oxfordxml',  [("<article-title>","</article-title>"),("<p>","</p>")]),
    ('PLOSxml',  [("<p>","</p>")])
#    ('RSE',       [("<xocs:rawtext>","</xocs:rawtext>")]),
#RSE is to big for testing, uncomment later
    ]


#Create directory for output
p = Path(output_folder)
try:
    p.mkdir()
except FileExistsError as exc:
    print(exc)

#keeps track of stats to report
stats1 = [0] * len(input_dirs)
stats2 = [0] * len(input_dirs)


#Open test files
for idx, folder in enumerate(input_dirs):
    directory = r'./' + folder[0]
    directory2 = r'./' + output_folder
    
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            #only do .xml files
            if not filename.endswith(".xml"):
                continue
            with open(root + '/' + filename, 'r',errors='ignore') as file:
                tagFound = False
                #Check for match
                line = file.read()
                print(filename)
                f = open(directory2 + '/' + folder[0] + filename,"w")
                for tags in folder[1]:
                    results = re.findall(tags[0] + '.*' + tags[1],line)
                    for result in results:
                        #Send output to test file
                        if result:
                            f.write(result[len(tags[0]):-len(tags[1])])
                            print('\t' + tags[0] + " found")
                            tagFound = True
                        else:
                            print('\t' + tags[0] + " not found")
                f.close()
                stats1[idx]+=1
                if tagFound == True:
                    stats2[idx]+=1
                else:
                    print("NO TAGS FOUND")
for idx, folder in enumerate(input_dirs):
    print(folder[0] + ":: " + str(stats1[idx]) + " files with " + str(stats2[idx]) + " found with at least one tag")
