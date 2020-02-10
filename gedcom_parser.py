""" 
Himanshu Rana 
"I pledge my honor that I have abided by the Stevens Honor System"


This program takes in a file (.ged) and parses it to make sure 
that the correct tags are valid given there level 
   
   
"""

import os
import csv
#create a dictionary that stores the values of each of the tags 

dict = {

        'NOTE':'0',
        'HEAD':'0',
        'TRLR':'0',
        'FAM':'0',
        'INDI':'0',
        'NAME':'1',
        'SEX':'1',
        'BIRT':'1',
        'DEAT':'1',
        'HUSB':'1',
        'WIFE':'1',
        'MARR':'1',
        'DIV':'1',
        'CHIL':'1',    
        'FAMC':'1',
        'FAMS':'1',
        'DATE':'2'
        }

fname = input("Enter file name: ")


workFile = open(fname)
output = open('parsed_output.txt', 'w+')
output_lines = []

#check to see if the file is empty 
#if so then exit. if not then continue parsing 
if os.stat(fname).st_size == 0 :
    print("Empty file")
    exit()
else :
    workFile.seek(0)
    for line in workFile :
       
        line = line.rstrip()
        #print out the current line 
        output.write('--> ' + line + '\n')
        output_lines.append('--> ' + line + '\n')
        #splitting up the line into appropriate
        info = line.split()
        level = info[0]
        #getting the keys 
        keys = dict.keys()

        #going through each line 
        for curr_key in keys :
            #checking to see if the key is in the dictionary 
            if curr_key in line and dict[curr_key] == level and curr_key in info :
                #extra checking if hte key is indi or fam 
                if (curr_key == 'INDI' or curr_key == 'FAM') :

                    #checking validity of each tag on its line 
                    if line.endswith(curr_key) :
                        validity = 'Y'
                        tag = curr_key
                        args = info[1]
                        break

                    else :
                        validity = 'N'
                        tag = curr_key
                        #selecting where to split each line 
                        #to seperate the rest of the arguements 
                        args = line.split(tag, 1)[1].lstrip()
                        break

                validity = 'Y'
                tag = curr_key
                args = line.split(tag, 1)[1].lstrip()
                break

            else :
                validity = 'N'
                tag = info[1]
                args = ''
                for x in info[2:] :
                    args += x + ' '

        output.write('<-- ' + level + '|' + tag + '|' + validity + '|' + args + '\n')
        output_lines.append('<-- ' + level + '|' + tag + '|' + validity + '|' + args + '\n')

#print(output_lines)

