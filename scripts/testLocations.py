#!/usr/bin/python3

import json, os
import geopy.distance
import csv

os.chdir('../')

key_file = "tests/jmap_data.json"

data_file = "tests/countnames_output.txt"

article_file = "tests/article_names.json"

output_file = open("tests/test1.txt",'w')

answer_key = json.load(open(key_file, 'r'))

parser_data = json.load(open(data_file, 'r'))

article_names = json.load(open(article_file, 'r'))

wrong_answers = open("tests/wrong_answers.txt",'w+')

count = 0
full_article_count = 0


def wrong_answer(top_name,data,answer,full_article_file,best_name):
    wrong_answers.write("Wrong answer in file "+full_article_file+"\n")
    wrong_answers.write("Article name: " + answer["title"]+"\n")
    wrong_answers.write("\tGuessed " + top_name+"\n")
    wrong_answers.write("\tPossible answers:"+"\n")
    for name in data:
        wrong_answers.write("\t\t"+name+"\n")
    wrong_answers.write("\tCorrect location is closest to possible answer " + best_name + "\n")
    wrong_answers.write("\tCorrect location at (" + answer["latitude"] +", " + answer["longitude"] + ")\n")
    wrong_answers.write("\tGuessed location at (" + data[top_name]["lat"] +", " + data[top_name]["lon"] + ")\n")
    
def print_no_guess(answer,full_article_file):
    wrong_answers.write("No answer for file "+full_article_file+"\n")
    wrong_answers.write("Article name: " + answer["title"]+"\n")
    wrong_answers.write("\tCorrect location at (" + answer["latitude"] +", " + answer["longitude"] + ")\n")


def print_stats(data,count,full_article_only):
    results = 0
    wrong = 0
    within_1000 = 0
    within_500 = 0
    within_161 = 0
    same_country = 0
    for i in data:
        tmp=data[i]
        if(full_article_only and not tmp['full_article']):
            continue
        distance = tmp['distance_km']
        if(distance>=1000):
            wrong+=1   
        if(distance<1000):
            within_1000+=1
        if(distance<500):
            within_500+=1
        if(distance<161):
            within_161+=1
        if(tmp['country_guess'] == tmp['country_jmap']):
            same_country+=1
        results+=1
    output_file.write("Out of " + str(count) + " articles: \n")
    output_file.write("\t" + str(count-results) + " had no result (" + str(round((count-results)/count*100,2)) + "%)\n")
    output_file.write("\t" + str(results) + " had a result (" + str(round(results/count*100,2)) + "%)\n")
    output_file.write("\t\t" + str(wrong) + " are outside of 1000 km (" + str(round(wrong/results*100,2)) + "%)\n")
    output_file.write("\t\t" + str(within_1000) + " are within 1000 km (" + str(round(within_1000/results*100,2)) + "%)\n")
    output_file.write("\t\t" + str(within_500) + " are within 500 km (" + str(round(within_500/results*100,2)) + "%)\n")
    output_file.write("\t\t" + str(within_161) + " are within 161 km (" + str(round(within_161/results*100,2)) + "%)\n")
    output_file.write("\t\t" + str(same_country) + " are in the same country (" + str(round(same_country/results*100,2)) + "%)\n")  
    
output = {}


for idx in answer_key:
    full_article = False
    answer = answer_key[idx]
    if(answer['title'] in article_names):
        full_article = True
        full_article_count+=1
    elif(answer["no_abstract"] == "1"): #does not have an abstract
        continue
    count+=1
    if(full_article):
        full_article_file = ""
        data = {}
        for article in article_names[answer['title']]:
            if(full_article_file):
                full_article_file += " AND " + article
            else:
                full_article_file = article
            try:
                temp1 = data
                temp2 = parser_data["/JournalMap/CS480/geoparser_output/" + article + "_output.txt"]
                data = {**temp1, **temp2} #only works on python 3.5+
                for i in data:
                    try:
                        data[i]['count'] = temp1[i]['count'] + temp2[i]['count']
                    except:
                        continue
            except:
                continue
        if(not data):
            full_article = False
            #print("Why is there no: " + "/JournalMap/CS480/geoparser_output/" + full_article_file + "_output.txt")
            print_no_guess(answer,full_article_file)
    if(not full_article):
        try:
            data = parser_data["/JournalMap/CS480/geoparser_output/jmap/jmap_" + str(idx) + "_output.txt"]
        except:
            continue
    top_name = max(data, key=lambda i: data[i]['count'])
    distance = geopy.distance.distance((data[top_name]['lat'],data[top_name]['lon']),(answer['latitude'],answer['longitude'])).km
    country_guess = data[top_name]['country_code3']
    
    best_name = min(data, key=lambda i: geopy.distance.distance((data[i]['lat'],data[i]['lon']),(answer['latitude'],answer['longitude'])).km)
    
    if(distance>=1000 and full_article):
        wrong_answer(top_name,data,answer,full_article_file,best_name)
    
    output[idx] = {}
    output[idx]['id'] = idx
    output[idx]['guessed_name'] = top_name
    output[idx]['lat_guess'] = data[top_name]['lat']
    output[idx]['long_guess'] = data[top_name]['lon']
    output[idx]['country_guess'] = country_guess
    output[idx]['lat_jmap'] = answer['latitude']
    output[idx]['long_jmap'] = answer['longitude']
    output[idx]['country_jmap'] = answer['alpha3_country']
    output[idx]['distance_km'] = distance
    output[idx]['full_article'] = full_article
    output[idx]['best_name'] = best_name

print_stats(output,count,False)
print_stats(output,full_article_count,True)


fieldnames=['id', 'guessed_name','lat_guess','long_guess','country_guess','lat_jmap','long_jmap','country_jmap','distance_km','full_article','best_name']
writer = csv.DictWriter(output_file,fieldnames=fieldnames)
writer.writeheader()
for item in output:
    writer.writerow(output[item])

output_file.close()