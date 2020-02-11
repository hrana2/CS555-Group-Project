"""
Himanshu Rana
"I pledge my honor that I have abided by the Stevens Honor System"


This program takes in a file (.ged) and parses it to make sure
that the correct tags are valid given there level


"""

import os
import csv
from prettytable import PrettyTable
#create a dictionary that stores the values of each of the tags

dict = {'NOTE':'0', 'HEAD':'0', 'TRLR':'0', 'FAM':'0', 'INDI':'0', 'NAME':'1', 'SEX':'1', 'BIRT':'1', 'DEAT':'1', 'HUSB':'1', 'WIFE':'1', 'MARR':'1', 'DIV':'1', 'CHIL':'1', 'FAMC':'1', 'FAMS':'1', 'DATE':'2'}

fname = input("Enter file name: ")
print(fname)

workFile = open(fname)
output = open('parsed_output.txt', 'w+')
output_lines = []


individual_table = PrettyTable()
individual_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

family_table = PrettyTable()
family_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]


def validation(line):

        #splitting up the line into appropriate
        info = line.split()
        level = info[0]
        #getting the keys
        keys = dict.keys()

        #going through each line
        for curr_key in keys:
            #checking to see if the key is in the dictionary
            if curr_key in line and dict[curr_key] == level and curr_key in info :
                #extra checking if the key is indi or fam
                if (curr_key == 'INDI' or curr_key == 'FAM') :
                    #checking validity of each tag on its line
                    if line.endswith(curr_key):
                        validity = 'Y'
                        tag = curr_key
                        args = info[1]

                        return [validity, level, tag, args]

                    else :
                        validity = 'N'
                        tag = curr_key
                        #selecting where to split each line
                        #to seperate the rest of the arguements
                        args = line.split(tag, 1)[1].lstrip()
                        return [validity, level, tag, args]

                validity = 'Y'
                tag = curr_key
                args = line.split(tag, 1)[1].lstrip()
                # Valid
                return [validity, level, tag, args]

        # Not valid tag
        validity = 'N'
        tag = info[1]
        args = ''
        for x in info[2:] :
            args += x + ' '
        return [validity, level, tag, args]



def parse_to_text(workFile):
    workFile.seek(0)
    for line in workFile:
        line = line.rstrip()
        #print out the current line
        output.write('--> ' + line + '\n')
        output_lines.append('--> ' + line + '\n')
        outVal = validation(line)
        print(outVal)
        curr_line = '<-- ' + outVal[1] + '|' + outVal[2] + '|' + outVal[0] + '|' + outVal[3] + '\n'
        output.write(curr_line)
        output_lines.append(curr_line)


def validate_to_array(workFile):
    outList = []
    for line in workFile:
        line = line.rstrip()
        outList.append(validation(line))
    return outList

def parse_to_chart(workFile):
    outList = validate_to_array(workFile)
    currEntry = 0
    while currEntry < len(outList):
        indiObj = {"ID":"", "Name":"", "Gender":"", "Birthday":"", "Age":"", "Alive":"", "Death":"", "Child":"", "Spouse":""}
        famObj = {"ID":"", "Married":"", "Divorced":"", "Husband ID":"", "Husband Name":"", "Wife ID":"", "Wife Name":"", "Children":""}
        if outList[currEntry][1] == "0":
            # if individual
            if outList[currEntry][2] == "INDI":
                while outList[currEntry+1][1] != "0":
                    if outList[currEntry][2] == "INDI":
                        indiObj["ID"] = outList[currEntry][3]
                    if outList[currEntry][2] == "NAME":
                        indiObj["Name"] = outList[currEntry][3]
                    if outList[currEntry][2] == "SEX":
                        indiObj["Gender"] = outList[currEntry][3]
                    if outList[currEntry][2] == "BIRT":
                        indiObj["Birthday"] = outList[currEntry][3]
                    if outList[currEntry][2] == "DEAT":
                        indiObj["Death"] = outList[currEntry][3]
                    if outList[currEntry][2] == "CHIL":
                        indiObj["Child"] = outList[currEntry][3]
                    if outList[currEntry][2] == "HUSB":
                        indiObj["Spouse"] = outList[currEntry][3]
                    if outList[currEntry][2] == "WIFE":
                        indiObj["Spouse"] = outList[currEntry][3]

                    currEntry += 1

                individual_table.add_row([indiObj["ID"],indiObj["Name"],indiObj["Gender"],indiObj["Birthday"],indiObj["Age"],indiObj["Alive"],indiObj["Death"],indiObj["Child"],indiObj["Spouse"]])

            #If fam
            if outList[currEntry][2] == "FAM":
                while outList[currEntry+1][1] != "0":
                    if outList[currEntry][2] == "FAM":
                        famObj["ID"] = outList[currEntry][3]
                    if outList[currEntry][2] == "MARR":
                        famObj["Married"] = outList[currEntry][3]
                    if outList[currEntry][2] == "DIV":
                        famObj["Divorced"] = outList[currEntry][3]
                    if outList[currEntry][2] == "HUSB":
                        famObj["Husband ID"] = outList[currEntry][3]
                    if outList[currEntry][2] == "HUSB":
                        famObj["Husband Name"] = outList[currEntry][3]
                    if outList[currEntry][2] == "WIFE":
                        famObj["Wife ID"] = outList[currEntry][3]
                    if outList[currEntry][2] == "WIFE":
                        famObj["Wife Name"] = outList[currEntry][3]
                    if outList[currEntry][2] == "CHIL":
                        famObj["Children"] = outList[currEntry][3]

                    currEntry += 1
                family_table.add_row([famObj["ID"],famObj["Married"],famObj["Divorced"],famObj["Husband ID"],famObj["Husband Name"],famObj["Wife ID"],famObj["Wife Name"],famObj["Children"]])
        currEntry += 1

#print(validate_to_array(workFile))
#print(parse_to_text(workFile))
print(parse_to_chart(workFile))
print(individual_table)
print(family_table)
