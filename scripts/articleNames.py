#this is a quickly thrown together script based on getRawText.py that compiles a lookup dictionary of the article names and file names
import sys
import os
import re
import json
from pathlib import Path

os.chdir('../')

output_file = 'tests/article_names.json'

input_dirs = [
    'Geoderma',
    'AOUxml',
    'Oxfordxml',
    'PLOSxml',
    'RSE'
    ]
title_tags = [
    ('<dc:title>','</dc:title>'),
    ('<article-title>','</article-title>')
]
xml_tags = re.compile('<.*?>')

output = {}

for idx, folder in enumerate(input_dirs):
    directory = r'./' + folder
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            #only do .xml files
            if not filename.endswith(".xml"):
                continue
            with open(root + '/' + filename, 'r',errors='ignore') as file:
                #Check for match
                line = file.read()
                print(filename)
                for tags in title_tags: # List of tuples representing the desired tags
                    results = re.findall(tags[0] + '.*' + tags[1],line) # Pull out the text between desired tags
                    for title in results:
                        tmp = re.sub(xml_tags, '', title)
                        if tmp not in output:
                            output[tmp] = []
                        output[tmp].append(folder+filename[:-4])
                file.close()


json.dump(output, open(output_file,'w'), indent='    ')


#temp testing code
"""jmap_data = json.load(open('tests/jmap_data.json','r'))

count=0
for entry in jmap_data:
    try:
        output[jmap_data[entry]['title']]
        print(jmap_data[entry]['title'])
        count+=1
    except:
        pass
print(count)
"""