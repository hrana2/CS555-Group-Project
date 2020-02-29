"""
Himanshu Rana, Evan Lewis, Kyle Bernardes, and Esti Stolbach
"I pledge my honor that I have abided by the Stevens Honor System"
This program takes in a file (.ged) and parses it to make sure
that the correct tags are valid given there level
"""

import os
import csv
from prettytable import PrettyTable
from datetime import datetime,date
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

individuals_array = []
families_array = []



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

id_match = []

def parse_to_chart(workFile):
    outList = validate_to_array(workFile)
    currEntry = 0

    children_id = []
    while currEntry < len(outList):
        indiObj = {"ID":"", "Name":"", "Gender":"", "Birthday":"", "Age":"", "Alive":"", "Death":"", "Child":"", "Spouse":""}
        #Children is a list so that you can add more than one child to the field if applicable
        famObj = {"ID":"", "Married":"", "Divorced":"", "Husband ID":"", "Husband Name":"", "Wife ID":"", "Wife Name":"", "Children":[]}


        if outList[currEntry][0] != "N": 
            if outList[currEntry][1] == "0":
                # if individual
                if outList[currEntry][2] == "INDI":
                    while outList[currEntry+1][1] != "0":
                        if outList[currEntry][2] == "INDI":
                            indiObj["ID"] = outList[currEntry][3]
                            name = outList[currEntry+1][3]
                            id_match.append(indiObj["ID"])
                            id_match.append(name)
                        if outList[currEntry][2] == "NAME":
                            indiObj["Name"] = outList[currEntry][3]
                        if outList[currEntry][2] == "SEX":
                            indiObj["Gender"] = outList[currEntry][3]
                        if outList[currEntry][2] == "BIRT":
                            indiObj["Birthday"] = outList[currEntry+1][3]

                            today = date.today()
                            bday = datetime.strptime(indiObj["Birthday"], '%d %b %Y')

                            age = (today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day)))


                            indiObj["Age"] = age

                            if outList[currEntry+2][2] != "DEAT":
                                indiObj["Alive"] = "Y"
                                indiObj["Death"] = "N/A"





                        if outList[currEntry][2] == "DEAT":
                            if outList[currEntry+1][2] == "DATE":
                                indiObj["Death"] = outList[currEntry+1][3]
                                indiObj["Alive"] = "N"
                                dod = datetime.strptime(indiObj["Death"], '%d %b %Y')
                                afterlife = (today.year - dod.year - ((today.month, today.day) < (dod.month, dod.day)))
                                died_at = abs(afterlife - age)
                                indiObj["Age"] = died_at



                        #if outList[currEntry][2] == "HUSB":
                            #indiObj["Spouse"] = outList[currEntry][3]
                        #if outList[currEntry][2] == "WIFE":
                            #indiObj["Spouse"] = outList[currEntry][3]


                        currEntry += 1
                    if outList[currEntry][2] == "FAMC":
                        indiObj["Child"] = outList[currEntry][3]

                    if outList[currEntry][2] == "FAMS":
                        indiObj["Spouse"] = outList[currEntry][3]




                    individual_table.add_row([indiObj["ID"],indiObj["Name"],indiObj["Gender"],indiObj["Birthday"],indiObj["Age"],indiObj["Alive"],indiObj["Death"],indiObj["Child"],indiObj["Spouse"]])


                #If fam
                if outList[currEntry][2] == "FAM":
                    while outList[currEntry+1][1] != "0":
                        if outList[currEntry][2] == "FAM":
                            famObj["ID"] = outList[currEntry][3]
                        if outList[currEntry][2] == "MARR":
                            famObj["Married"] = outList[currEntry+1][3]
                            famObj["Divorced"] = "N/A"
                        if outList[currEntry][2] == "DIV":
                            famObj["Divorced"] = outList[currEntry+1][3]

                        if outList[currEntry][2] == "HUSB":
                            famObj["Husband ID"] = outList[currEntry][3]
                        if outList[currEntry][2] == "HUSB":
                            for i in range(len(id_match)):
                                if famObj["Husband ID"] == id_match[i]:
                                    famObj["Husband Name"] = id_match[i+1]
                        if outList[currEntry][2] == "WIFE":
                            famObj["Wife ID"] = outList[currEntry][3]

                        if outList[currEntry][2] == "WIFE":
                            for i in range(len(id_match)):
                                if famObj["Wife ID"] == id_match[i]:
                                    famObj["Wife Name"] = id_match[i+1]

                        if outList[currEntry][2] == "CHIL":
                             famObj["Children"].append(outList[currEntry][3])

                        currEntry += 1



                    family_table.add_row([famObj["ID"],famObj["Married"],famObj["Divorced"],famObj["Husband ID"],famObj["Husband Name"],famObj["Wife ID"],famObj["Wife Name"],famObj["Children"]])

        currEntry += 1

    #print(outList)
    #print(id_match)
    #print(children_id)




def parse_to_objects(workFile):
    outList = validate_to_array(workFile)
    currEntry = 0

    children_id = []
    
    while currEntry < len(outList):
        indiObj = {"ID":"", "Name":"", "Gender":"", "Birthday":"", "Age":"", "Alive":"", "Death":"", "Child":"", "Spouse":""}
        #Children is a list so that you can add more than one child to the field if applicable
        famObj = {"ID":"", "Married":"", "Divorced":"", "Husband ID":"", "Husband Name":"", "Wife ID":"", "Wife Name":"", "Children":[]}


        if outList[currEntry][0] != "N": 
            if outList[currEntry][1] == "0":
                # if individual
                if outList[currEntry][2] == "INDI":
                    while outList[currEntry+1][1] != "0":
                        if outList[currEntry][2] == "INDI":
                            indiObj["ID"] = outList[currEntry][3]
                            name = outList[currEntry+1][3]
                            id_match.append(indiObj["ID"])
                            id_match.append(name)
                        if outList[currEntry][2] == "NAME":
                            indiObj["Name"] = outList[currEntry][3]
                        if outList[currEntry][2] == "SEX":
                            indiObj["Gender"] = outList[currEntry][3]
                        if outList[currEntry][2] == "BIRT":
                            indiObj["Birthday"] = outList[currEntry+1][3]

                            today = date.today()
                            bday = datetime.strptime(indiObj["Birthday"], '%d %b %Y')

                            age = (today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day)))


                            indiObj["Age"] = age

                            if outList[currEntry+2][2] != "DEAT":
                                indiObj["Alive"] = "Y"
                                indiObj["Death"] = "N/A"





                        if outList[currEntry][2] == "DEAT":
                            if outList[currEntry+1][2] == "DATE":
                                indiObj["Death"] = outList[currEntry+1][3]
                                indiObj["Alive"] = "N"
                                dod = datetime.strptime(indiObj["Death"], '%d %b %Y')
                                afterlife = (today.year - dod.year - ((today.month, today.day) < (dod.month, dod.day)))
                                died_at = abs(afterlife - age)
                                indiObj["Age"] = died_at



                        #if outList[currEntry][2] == "HUSB":
                            #indiObj["Spouse"] = outList[currEntry][3]
                        #if outList[currEntry][2] == "WIFE":
                            #indiObj["Spouse"] = outList[currEntry][3]


                        currEntry += 1
                    if outList[currEntry][2] == "FAMC":
                        indiObj["Child"] = outList[currEntry][3]

                    if outList[currEntry][2] == "FAMS":
                        indiObj["Spouse"] = outList[currEntry][3]

                    individuals_array.append(indiObj)


                #If fam
                if outList[currEntry][2] == "FAM":
                    while outList[currEntry+1][1] != "0":
                        if outList[currEntry][2] == "FAM":
                            famObj["ID"] = outList[currEntry][3]
                        if outList[currEntry][2] == "MARR":
                            famObj["Married"] = outList[currEntry+1][3]
                            famObj["Divorced"] = "N/A"
                        if outList[currEntry][2] == "DIV":
                            famObj["Divorced"] = outList[currEntry+1][3]

                        if outList[currEntry][2] == "HUSB":
                            famObj["Husband ID"] = outList[currEntry][3]
                        if outList[currEntry][2] == "HUSB":
                            for i in range(len(id_match)):
                                if famObj["Husband ID"] == id_match[i]:
                                    famObj["Husband Name"] = id_match[i+1]
                        if outList[currEntry][2] == "WIFE":
                            famObj["Wife ID"] = outList[currEntry][3]

                        if outList[currEntry][2] == "WIFE":
                            for i in range(len(id_match)):
                                if famObj["Wife ID"] == id_match[i]:
                                    famObj["Wife Name"] = id_match[i+1]

                        if outList[currEntry][2] == "CHIL":
                             famObj["Children"].append(outList[currEntry][3])

                        currEntry += 1

                    families_array.append(famObj)

        currEntry += 1




def test_validate_to_array():
    print(validate_to_array(workFile))



def test_parse_to_chart():
    print(parse_to_chart(workFile))
    with open("tables.txt", "w") as tables:
        tables.write(str(individual_table))
        tables.write(str(family_table))
        tables.close()
    print("individuals Table\n")
    print(individual_table)
    print("Family Table\n")
    print(family_table)

def test_parse_to_objects():
    print(parse_to_objects(workFile))
    print("individuals Array\n")
    print(individuals_array)
    print("Family Array\n")
    print(families_array)



def us02_birth_b4_marriage(fam):
    #Store birth date
    #Store marriage date
    #Compare birth and marriage dates
    mday = fam["Married"]

    husband_id = fam["Husband ID"]
    wife_id = fam["Wife ID"]

    husband = None
    wife = None
    for indi in individuals_array:
        if indi['ID'] == husband_id:
            husband = indi
        if indi['ID'] == wife_id:
            wife = indi
        if husband and wife:
            break
    bday1 = husband["Birthday"]
    bday2 = wife["Birthday"]

    if bday1 < mday and bday2 < mday:
        return True
    return False

def us03_birth_b4_death(indi):
    #Store birth date
    #Store death date
    #Compare birth and death dates
    #bday = indi["Birthday"]

    if indi["Death"] != "N/A":
        dod = indi["Death"]
        dob = indi["Birthday"]
        #dday = indi["Death"]
        if dob > dod:
            return False
        return True
    return True

def us04_marr_b4_divorce(fam):
    #Compare marriage date to divorce date
    if fam["Divorced"] != "N/A":
        dom = fam["Married"]
        dod = fam["Divorced"]
        if dom > dod:
            return False
        return True
    return True

def us05_marr_b4_death(fam):
        #Find marriage date
        #Find if either/both spouses are dead
        #Compare marriage date to death date
    marriageDate = datetime.strptime(fam["Married"], '%d %b %Y')

    husband_id = fam["Husband ID"]
    wife_id = fam["Wife ID"]

    husband = None
    wife = None
    for indi in individuals_array:
        if indi['ID'] == husband_id:
            husband = indi
        if indi['ID'] == wife_id:
            wife = indi
        if husband and wife:
            break

    if husband["Death"] != "N/A":
        death_date_h = datetime.strptime(husband["Death"], '%d %b %Y')
        if marriageDate > death_date_h:
            return -1

    if wife["Death"] != "N/A":
        death_date_w = datetime.strptime(wife["Death"], '%d %b %Y')
        if marriageDate > death_date_w:
            return 1
    return 0


def us06_div_b4_death(fam):
    #Find divorce date if applicable
    #Find if either/both spouses are dead
    #Compare divorce date to death date and make sure divore comes first


    if fam["Divorced"] != "N/A": 
        divorceDate = datetime.strptime(fam["Divorced"], '%d %b %Y')

        if divorceDate != 'N/A': 
            husband_id = fam["Husband ID"]
            wife_id = fam["Wife ID"]

            husband = None
            wife = None

            for indi in individuals_array:
                if indi['ID'] == husband_id:
                    husband = indi
                if indi['ID'] == wife_id:
                    wife = indi
                if husband and wife:
                    break

            if husband["Death"] != "N/A":
                death_date_h = datetime.strptime(husband["Death"], '%d %b %Y')
                if divorceDate > death_date_h: 
                    return -1

            if wife["Death"] != "N/A":
                death_date_w = datetime.strptime(wife["Death"], '%d %b %Y')
                if divorceDate > death_date_w: 
                    return 1
    return 0


  
def us07_less_than_150(indi):

    today = date.today()
    bday = datetime.strptime(indi["Birthday"], '%d %b %Y')

    age = (today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day)))


    if age >= 150:
        return False
    return True


def us08_birth_b4_marr_parents(indi,fam):
    # get birth date of individual
    # get marriage of parents
    # get divorce of parents
    # no birth more than 9 months after divorce

    # ensure individual is in family
    if(fam["ID"] == indi["Child"]):
        birthDate = datetime.strptime(indi["Birthday"], '%d %b %Y')
        marriedDate = datetime.strptime(fam["Married"], '%d %b %Y')
        if(marriedDate > birthDate):
            return -1
        elif(fam["Divorced"] != "N/A"):
            divorceDate = datetime.strptime(fam["Divorced"], '%d %b %Y')
            if ((birthDate - divorceDate).years > 0 or (birthDate - divorceDate).months >= 9):
                return 0
        else:
            return 1
    return



def us09_birth_b4_death_parents(indi,fam, individuals):
    if(fam["ID"] == indi["Child"]):
        birthDate = datetime.strptime(indi["Birthday"], '%d %b %Y')
        momID = fam["Wife ID"]
        dadID = fam["Husband ID"]
        
        mom = {"ID":"", "Name":"", "Gender":"", "Birthday":"", "Age":"", "Alive":"", "Death":"", "Child":"", "Spouse":""}
        # is mom alive if not get the date of death
        for x in individuals:
            if(x["ID"] == momID):
                mom = x
                break
        if(mom["Alive"] == "N"):
            momDeath = datetime.strptime(mom["Death"], '%d %b %Y')
            momAlive = False
        else:
            momAlive = True

        if(momAlive == False):
            if(momDeath < birthDate):
                return 0
        
        dad = {"ID":"", "Name":"", "Gender":"", "Birthday":"", "Age":"", "Alive":"", "Death":"", "Child":"", "Spouse":""}
        for x in individuals:
            if(x["ID"] == dadID):
                dad = x
                break
        if(dad["Alive"] == "N"):
            dadDeath = datetime.strptime(dad["Death"], '%d %b %Y')
            dadAlive = False
        else:
            dadAlive = True

        if(dadAlive == False):
            if((birthDate.year - dadDeath.year) > 0 or (birthDate.month - dadDeath.month) >= 9):
                return 1

    return



####    TEST CASES #####


test_parse_to_chart()


# test_us02_birth_b4_marriage()
# test_us03_birth_b4_death()

# test_us04_marr_b4_divorce()
# test_us05_marr_b4_death()
# test_us06_div_b4_death()
# test_us07_less_than_150()
# test_us08_birth_b4_marr_parents()
# test_us09_birth_b4_death_parents()






# #test_validate_to_array()


# validate_to_array(workFile)

#parse_to_objects(workFile)
#test_parse_to_objects()


