#we were provided CSV files that are used internaly by JournalMap
#they contain the abstract of each article along with the geolocation in the database
#this program turns the CSV into a python object and takes only the abstract and the geolocation
import sys
import os
import csv
import json

os.chdir('../')

#this program expects two CVE files called jmap_articles and jmap_locations in a folder called jmap in the project folder
input_folder = 'jmap'
input_files = (
    ('jmap_articles.csv','article'),
    ('jmap_locations.csv','location')
)
output_folder = 'processed_files/Jmap'
output_file = 'jmap_data.json'

os.chdir('./'+input_folder)

#this section goes though the input files and removes newlines
#that are not at the end of the data for each article
for file in input_files:
    out_file = open(file[0] + '2','w')
    for line in open(file[0],'r',errors='ignore'):
        fields = 0
        for char in line:
            if(char == '|'):
                fields+=1
                out_file.write(char)
            elif(fields < 28 and char == '\n' or char == '\r'):
                out_file.write(' ')
            else:
                out_file.write(char)
    out_file.close()

#this fills out the data dictionary
#the data dictionary has records numbered with the id
#each record has article and location as it's members
#article and location have the tags from their respective files
data = {}
for file in input_files:
    with open(file[0] + '2', 'r',newline='',errors='ignore') as a_file:
        articles  = csv.DictReader(a_file, delimiter='|')
        last_id = 0
        for article in articles:
            try:
                a_id = int(article['id'])
            except ValueError:
                print('Bad id: ' + article['id'])
                continue
            if not a_id in data:
                data[a_id] = {}
            data[a_id][file[1]] = article

#stores the data structure for later use
data2 = {}
for i in data:
    try:
      data[i][input_files[0][1]]
      data[i][input_files[1][1]]
    except KeyError:
        print('Incomplete data for ' + str(i))
        continue
    data2[i]={}
    data2[i]['id']=data[i][input_files[0][1]]['id']
    data2[i]['title']=data[i][input_files[0][1]]['title']
    data2[i]['no_abstract']=data[i][input_files[0][1]]['no_abstract']
    data2[i]['country_id']=data[i][input_files[1][1]]['country_id']
    data2[i]['state_id']=data[i][input_files[1][1]]['state_id']
    data2[i]['latitude']=data[i][input_files[1][1]]['latitude']
    data2[i]['longitude']=data[i][input_files[1][1]]['longitude']

os.chdir('../')

json.dump(data2, open(output_file,'w'), indent='    ')

"""
#this section outputs the title and abstract into individual files

os.chdir('./' + output_folder)

for i in data:
    try:
      data[i][input_files[0][1]]
      data[i][input_files[1][1]]
    except KeyError:
        print('Incomplete data for ' + str(i))
        continue
    out_file = open('jmap_' + str(i) + '.xml','w')
    out_file.write(data[i][input_files[0][1]]['title'])
    out_file.write(data[i][input_files[0][1]]['abstract'])
    out_file.close
"""
