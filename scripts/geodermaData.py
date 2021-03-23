import sys
import os

#Open test file
file = open("10.1016.0016-7061(77)90034-9.xml")

#Check test file integrity
if file != None:
    print("No error. File found.")

#Test output file contents with a print
flag = False

with open('10.1016.0016-7061(77)90034-9.xml', 'r') as file:
    for line in file:
        for character in line:
            #Set flags for strings of characters we don't want to print
            if character == '<' and flag == False:
                flag = True
                continue
            elif character == '>' and flag == True:
                flag = False
                continue

            #Check flag and print to file
            if flag == False:
                #Print to test output
                print(character, end='')
                #Send output to test file
                f = open("output.txt","a")
                f.write(character)
                f.close()
