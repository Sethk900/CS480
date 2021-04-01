#geodermaData.py
#Takes raw files from a directory specified manually in this script and sends
#output to a file called "./geoderma_processed" in the form of text that 
#follows the regex defined in this script.

import sys
import os
import re
from pathlib import Path

os.chdir('../')

#Create directory for output
p = Path('geoderma_processed')
try:
    p.mkdir()
except FileExistsError as exc:
    print(exc)

#Open test files
#ATTENTION: This must be entered in manually for each test set.
#The folder name MATTERS
directory = r'./Geoderma'
directory2 = r'./geoderma_processed'
for filename in os.listdir(directory):
    with open(directory + '/' + filename, 'r') as file:
        #Check for match
        line = file.read()
        result = re.search(r"<xocs:rawtext>.*</xocs:rawtext>",line)

        #Print success message for every file
        print(filename + ' completed')

        #Send output to test file
        if result:
            f = open(directory2 + '/' + filename,"w")
            f.write(result.group(0)[14:-15])
            f.close()
        else:
            print(filename + ' failed...')
