
"""
Himanshu Rana, Evan Lewis, Kyle Bernardes, and Esti Stolbach
"I pledge my honor that I have abided by the Stevens Honor System"
This program takes in a file (.ged) and parses it to make sure
that the correct tags are valid given there level
"""

import os
import csv
from prettytable import PrettyTable
from datetime import datetime,date,timedelta
#create a dictionary that stores the values of each of the tags

dict = {'NOTE':'0', 'HEAD':'0', 'TRLR':'0', 'FAM':'0', 'INDI':'0', 'NAME':'1', 'SEX':'1', 'BIRT':'1', 'DEAT':'1', 'HUSB':'1', 'WIFE':'1', 'MARR':'1', 'DIV':'1', 'CHIL':'1', 'FAMC':'1', 'FAMS':'1', 'DATE':'2'}

fname = input("Enter file name: ")
print(fname)

open('output.txt', 'w').close()
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

outList = validate_to_array(workFile)
currEntry = 0

id_match = []
famid_match = []
children_id = []

# setup individuals array first
while currEntry < len(outList):
    indiObj = {"ID":"", "Name":"", "Gender":"", "Birthday":"", "Age":"", "Alive":"", "Death":"", "Child":"", "Spouse":""}
    #Children is a list so that you can add more than one child to the field if applicable

    if outList[currEntry][0] != "N":
        if outList[currEntry][1] == "0":
            # if individual
            if outList[currEntry][2] == "INDI":
                while outList[currEntry+1][1] != "0":
                    if outList[currEntry][2] == "INDI":
                        indiObj["ID"] = outList[currEntry][3]
                        name = outList[currEntry+1][3]
                        id_match.append(indiObj["ID"])
                        #id_match.append(name)
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

    currEntry += 1

# now setup array of families
currEntry = 0
while currEntry < len(outList):
    famObj = {"ID":"", "Married":"", "Divorced":"", "Husband ID":"", "Husband Name":"", "Wife ID":"", "Wife Name":"", "Children":[]}

    if outList[currEntry][0] != "N":
        if outList[currEntry][1] == "0":
            #If fam
            if outList[currEntry][2] == "FAM":
                while outList[currEntry+1][1] != "0":
                    if outList[currEntry][2] == "FAM":
                        famObj["ID"] = outList[currEntry][3]
                        famid_match.append(famObj["ID"])
                    if outList[currEntry][2] == "MARR":
                        famObj["Married"] = outList[currEntry+1][3]
                        famObj["Divorced"] = "N/A"
                    if outList[currEntry][2] == "DIV":
                        famObj["Divorced"] = outList[currEntry+1][3]

                    if outList[currEntry][2] == "HUSB":
                        famObj["Husband ID"] = outList[currEntry][3]
                        name = ""
                        for i in individuals_array:
                            if i["ID"] == famObj["Husband ID"]:
                                name = i["Name"]
                        famObj["Husband Name"] = name
                    if outList[currEntry][2] == "WIFE":
                        famObj["Wife ID"] = outList[currEntry][3]
                        name = ""
                        for i in individuals_array:
                            if i["ID"] == famObj["Wife ID"]:
                                name = i["Name"]
                        famObj["Wife Name"] = name

                    if outList[currEntry][2] == "CHIL":
                         famObj["Children"].append(outList[currEntry][3])

                    currEntry += 1

                families_array.append(famObj)

    currEntry += 1

def parse_to_chart():
    for indi in individuals_array:
        individual_table.add_row([indi["ID"],indi["Name"],indi["Gender"],indi["Birthday"],indi["Age"],indi["Alive"],indi["Death"],indi["Child"],indi["Spouse"]])
    for fam in families_array:
        family_table.add_row([fam["ID"],fam["Married"],fam["Divorced"],fam["Husband ID"],fam["Husband Name"],fam["Wife ID"],fam["Wife Name"],fam["Children"]])

    #print(outList)
    #print(id_match)
    #print(children_id)
    #print(individual_table)
    #print(family_table)
    with open("output.txt", "a") as tables:
        tables.write(str(individual_table) + "\n")
        tables.write(str(family_table) + "\n")
    return individual_table, family_table

parse_to_chart()

######## USER STORIES #########


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

def us_10_marriage_after_14(fam):
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

    husbandBirthDate = datetime.strptime(husband["Birthday"], '%d %b %Y')
    wifeBirthDate = datetime.strptime(wife["Birthday"], '%d %b %Y')

    marriedDate = datetime.strptime(fam["Married"], '%d %b %Y')

    if marriedDate-husbandBirthDate < timedelta(days=5110) or marriedDate-wifeBirthDate < timedelta(days=5110):
        return False
    return True


def us_11_no_bigamy(indi):
    indi_id = indi["ID"]
    husband_count = 0
    wife_count = 0

    for fam in families_array:
        if fam["Husband ID"] == indi_id:
            husband_count += 1
        if fam["Wife ID"] == indi_id:
            wife_count += 1

    if wife_count > 1 or husband_count > 1:
        return False
    return True




def us12_parents_not_too_old(fam, indi):
    if(fam["ID"] == indi["Child"]):
        childBirthDate = datetime.strptime(indi["Birthday"], '%d %b %Y')
        dad_id = fam["Husband ID"]
        mom_id = fam["Wife ID"]

        dad = None
        mom = None
        for indi in individuals_array:
            if indi['ID'] == dad_id:
                dad = indi
            if indi['ID'] == mom_id:
                mom = indi
            if dad and mom:
                break

        dadBirthDate = datetime.strptime(dad["Birthday"], '%d %b %Y')
        momBirthDate = datetime.strptime(mom["Birthday"], '%d %b %Y')
        if (childBirthDate.year - momBirthDate.year) > 59 or (childBirthDate.year - dadBirthDate.year) > 79:
            return False
        else:
            return True

    return

def us13_siblings_spacing(fam, indi):
    for child in individuals_array:
        if fam["ID"] == child["Child"] and indi["ID"] != child["ID"] and indi["Child"] == fam["ID"]:
            birthDate = datetime.strptime(indi["Birthday"], '%d %b %Y')
            childBirthDate = datetime.strptime(child["Birthday"], '%d %b %Y')
            if birthDate.year == childBirthDate.year:
                if abs(birthDate.month - childBirthDate.month) < 9 and abs(birthDate.day - childBirthDate.day) > 3:
                    return False
                else:
                    return True
    return True

def us14_multiple_births_lessthan_5(fam, individuals):
    if len(fam["Children"]) <= 5:
        return True
    else:
        birthdays = {}
        for sib in fam["Children"]:
            for indi in individuals:
                if sib == indi["ID"]:
                    if indi["Birthday"] in birthdays:
                        birthdays[indi["Birthday"]] += 1
                        if birthdays[indi["Birthday"]] > 5:
                            return False
                    else:
                        birthdays[indi["Birthday"]] = 1
    return True

def us15_fewer_than_15_siblings(fam):
    if len(fam["Children"]) >= 15:
        return False
    else:
        return True

def us16_male_last_names(fam):
    fam_last_name = fam["Husband Name"].split("/")[1]
    #print(fam["Husband Name"])
    #print(fam["Children"])
    for id in fam["Children"]:
        for indi in individuals_array:
            if indi["ID"] == id and indi["Gender"] == "M":
                #print(indi["Name"].split("/")[1])
                if fam_last_name != indi["Name"].split("/")[1]:
                    return False
                continue

def us17_no_marriages_to_children(fam):
    for child in fam["Children"]:
        if child == fam["Husband ID"] or  child == fam["Wife ID"]:
            return False
    return True

def us18_siblings_should_not_marry(indi):
    for sibling in individuals_array:
        if indi["ID"] != sibling["ID"] and indi["Child"] == sibling["Child"] and indi["Spouse"] == sibling["Spouse"]:
            return False
    return True

def us19_first_cousins_should_not_marry(indi1_id, indi2_id):
    #Find the two individual's parents
    indi1_father_id = None
    indi1_mother_id = None
    indi2_father_id = None
    indi2_mother_id = None
    for fam in families_array:
        for child_id in fam["Children"]:
            if child_id == indi1_id:
                indi1_father_id = fam["Husband ID"]
                indi1_mother_id = fam["Wife ID"]
            if child_id == indi2_id:
                indi2_father_id = fam["Husband ID"]
                indi2_mother_id = fam["Wife ID"]

    #Find the individuals parent's parents (total of 4 for each original individual
    indi1_grandfather1_id = None
    indi1_grandmother1_id = None
    indi1_grandfather2_id = None
    indi1_grandmother2_id = None
    indi2_grandfather1_id = None
    indi2_grandmother1_id = None
    indi2_grandfather2_id = None
    indi2_grandmother2_id = None



    for fam in families_array:
        for child_id in fam["Children"]:
            if child_id == indi1_father_id:
                indi1_grandfather1_id = fam["Husband ID"]
                indi1_grandmother1_id = fam["Wife ID"]
            if child_id == indi1_mother_id:
                indi1_grandfather2_id = fam["Husband ID"]
                indi1_grandmother2_id = fam["Wife ID"]

            if child_id == indi2_father_id:
                indi2_grandfather1_id = fam["Husband ID"]
                indi2_grandmother1_id = fam["Wife ID"]
            if child_id == indi2_mother_id:
                indi2_grandfather2_id = fam["Husband ID"]
                indi2_grandmother2_id = fam["Wife ID"]

    '''print("Indi1")
    print(indi1_grandfather1_id)
    print(indi1_grandmother1_id)
    print(indi1_grandfather2_id)
    print(indi1_grandmother2_id)
    print("indi2")
    print(indi2_grandfather1_id)
    print(indi2_grandmother1_id)
    print(indi2_grandfather2_id)
    print(indi2_grandmother2_id)'''

    #Check if any of the grandfathers are the same between the two individuals
    if indi1_grandfather1_id == indi2_grandfather1_id and indi1_grandfather1_id != None and indi2_grandfather1_id != None:
        return False

    if indi1_grandfather1_id == indi2_grandfather2_id and indi1_grandfather1_id != None and indi2_grandfather2_id != None:
        return False

    if indi1_grandfather2_id == indi2_grandfather1_id and indi1_grandfather2_id != None and indi2_grandfather1_id != None:
        return False

    if indi1_grandfather2_id == indi2_grandfather2_id and indi1_grandfather2_id != None and indi2_grandfather2_id != None:
        return False

    #Check if any of the grandmothers are the same between the two individuals
    if indi1_grandmother1_id == indi2_grandmother1_id and indi1_grandmother1_id != None and indi2_grandmother1_id != None:
        return False

    if indi1_grandmother1_id == indi2_grandmother2_id and indi1_grandmother1_id != None and indi2_grandmother2_id != None:
        return False

    if indi1_grandmother2_id == indi2_grandmother1_id and indi1_grandmother2_id != None and indi2_grandmother1_id != None:
        return False

    if indi1_grandmother2_id == indi2_grandmother2_id and indi1_grandmother2_id != None and indi2_grandmother2_id != None:
        return False

    #None of the grandparents are the same and thus they are not first cousins
    return True


def us21_correct_gender_role(fam):
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
    husb_gend = husband["Gender"]
    wife_gend = wife["Gender"]

    if husb_gend == 'F':
        return -1
    if wife_gend == 'M':
        return 0
    #return

def us22_unique_IDs(arr1, arr2):
    length1 = len(id_match)
    length2 = len(famid_match)

    for i in range(length1):
        for j in range(i + 1, length1):
            if arr1[i] == arr1[j]:
               return 1

    for x in range(length2):
        for y in range(x + 1, length2):
            if arr2[x] == arr2[y]:
                return 0
                #print(arr[i])
        #if x == "@I2@":

def us23_unique_name_and_birth_date(indi,individuals):
    for otherIndi in individuals:
        if(indi["Name"] == otherIndi["Name"] and indi["Birthday"] == otherIndi["Birthday"] and indi["ID"] != otherIndi["ID"]):           # same name and birthday but different person
            return False
    return True

def us24_unique_families_by_spouses(fam,families):
    for otherFam in families:
        if(fam["Husband Name"] == otherFam["Husband Name"] and fam["Wife Name"] == otherFam["Wife Name"] and fam["Married"] == otherFam["Married"] and fam["ID"] != otherFam["ID"]):
            return False
    return True

def us25_unique_first_names_in_families(fam):
    child_name_table = []
    child_birthday_table = []
    for child_id in fam["Children"]:
        for indi in individuals_array:
            if child_id == indi["ID"]:
                child_name_table.append(indi["Name"])
                child_birthday_table.append(indi["Birthday"])
    for i in range(0, len(child_name_table)):
        for j in range(i+1, len(child_name_table)):
            if(child_name_table[i] == child_name_table[j]):
                #print(child_name_table[j])
                return False
    for i in range(0, len(child_birthday_table)):
        for j in range(i+1, len(child_birthday_table)):
            if(child_birthday_table[i] == child_birthday_table[j]):
                #print(child_birthday_table[j])
                return False
    return True


def us26_corresponding_entries(indi, fam):
    if indi["Spouse"] == fam["ID"] and indi["ID"] == fam["Husband ID"] or indi["ID"] == fam["Wife ID"]:
        return True
    for child in fam["Children"]:
        if indi["Child"] == fam["ID"] and indi["ID"] == child:
            return True
    return False

def us27_include_individual_ages(indi):
    return indi["Age"]

def us28_order_siblings_by_age(fam):
    sibOrder = {}
    for sibling in fam["Children"]:
        for indi in individuals_array:
            if indi["ID"] == sibling:
                sibOrder[sibling] = indi["Age"]
    return sorted(sibOrder.values(), reverse = True)

def us29_list_deceased(indi):
    theDead = []
    for indi in individuals_array:
        if indi["Alive"] == 'N':
            theDead.append(indi["Name"])
    return theDead

def us32_list_multiple_births(individuals,fam):
    birthdays = {}
    for sib in fam["Children"]:
        for indi in individuals:
            if sib == indi["ID"]:
                if indi["Birthday"] in birthdays:
                    birthdays[indi["Birthday"]] += 1
                    if birthdays[indi["Birthday"]] > 5:
                        return False
                else:
                    birthdays[indi["Birthday"]] = 1

def us33_list_orphans(indi,fam):
    orphans = []
    # are parents dead
    for currFam in fam:
        for dad in indi:
            if(currFam["Husband ID"] == dad["ID"] and dad["Alive"] == "N"):
                for mom in indi:
                    if(currFam["Wife ID"] == mom["ID"] and mom["Alive"] == "N"):
                        # get age of children
                        for children in currFam["Children"]:
                            for child in indi:
                                if(child["ID"] == children and child["Alive"] == "Y" and child["Age"] < 18):
                                    orphans.append(child["Name"])
    return orphans

def us35_list_recent_births(indi):
    newbies = []

    today = datetime.today()

    for individ in individuals_array:
        bday = individ["Birthday"]
        dtbday_obj = datetime.strptime(bday, '%d %b %Y')
        if (today - dtbday_obj) <= timedelta(days=30):
            newbies.append(individ["Name"])
    return newbies

#print(datetime.today().date() - timedelta(days=30))

def us36_list_recent_deaths(indi):
    justDied = []

    today = datetime.today()
    for individ in individuals_array:
        if individ["Death"] != "N/A":
            dday = individ["Death"]
            dtbday_obj = datetime.strptime(dday, '%d %b %Y')
            if (today - dtbday_obj) <= timedelta(days=30):
                justDied.append(individ["Name"])
    return justDied

def us38_list_upcoming_birthdays(indi):
    soon_bdays = []

    curr_date = datetime.today()
    later_date = curr_date + timedelta(days=30)

    for individ in individuals_array:
        if individ["Alive"] == "Y":
            dtbday_obj = datetime.strptime(individ["Birthday"], '%d %b %Y')
        dtbday_obj = datetime(curr_date.year, dtbday_obj.month, dtbday_obj.day, 0, 0)
        if curr_date <= dtbday_obj <= later_date:
            soon_bdays.append(individ["Name"])
    return soon_bdays




############   TEST CASES #################


def test_us02_birth_b4_marriage():
    #parse_to_objects(workFile)
    file = open("output.txt", "a")
    for fam in families_array:
        result = us02_birth_b4_marriage(fam)
        if result == False:
             file.write("Error: Family: " + fam["ID"] +  ": US02: Birthday before married " + fam["Married"] + "\n")
             return "Error: Family: " + fam["ID"] +  ": US02: Birth before married " + fam["Married"]

    #file.close()

def test_us03_birth_b4_death():
    #parse_to_objects(workFile)
    file = open("output.txt", "a")
    for indi in individuals_array:
        result = us03_birth_b4_death(indi)
        if result == False:
            file.write("Error: Indi: " + indi["ID"] + " US03: Death " + indi["Death"] + " before Birthday " + indi["Birthday"] + "\n")
            return "Error: Indi: " + indi["ID"] + " US03: Death " + indi["Death"] + " before Birthday " + indi["Birthday"]
    #file.close()


def test_us04_marr_b4_divorce():
    #parse_to_objects(workFile)
    file = open("output.txt", "a")

    for fam in families_array:
        result = us04_marr_b4_divorce(fam)
        if result == False:
            file.write("Error: Family: " + fam["ID"] +  ": US04: Divorced " + fam["Divorced"] + " before married " + fam["Married"] + "\n")
            return "Error: Family: " + fam["ID"] +  ": US04: Divorced " + fam["Divorced"] + " before married " + fam["Married"]

    #file.close()

def test_us05_marr_b4_death():
    # parse_to_objects(workFile)
    file = open("output.txt", "a")

    for fam in families_array:
        result = us05_marr_b4_death(fam)
        if(result == -1):
            file.write("Error: Family: " + fam["ID"] + ": US05: Death of husband before married " + fam["Married"] + "\n")
            return "Error: Family: " + fam["ID"] + ": US05: Death of husband before married " + fam["Married"]
        elif(result == 1):
            file.write("Error: Family: " + fam["ID"] + ": US05: Death of wife before married " + fam["Married"] + "\n")
            return "Error: Family: " + fam["ID"] + ": US05: Death of wife before married " + fam["Married"]
    #file.close()

def test_us06_div_b4_death():
    #parse_to_objects(workFile)
    file = open("output.txt", "a")


    for fam in families_array:
        result = us06_div_b4_death(fam)
        if(result == 1 or result == -1):
            file.write("Error: Family: " + fam["ID"] + ": US06: Died before divorce " + fam["Divorced"] + "\n")
            return "Error: Family: " + fam["ID"] + ": US06: Died before divorce " + fam["Divorced"]
    #file.close()

def test_us07_less_than_150():
    #parse_to_objects(workFile)
    file = open("output.txt", "a")

    for indi in individuals_array:
        result = us07_less_than_150(indi)
        if result == False:
            file.write("Error: Individual: " + indi["ID"] + ": US07: Over 150 years old" + "\n")
            return "Error: Individual: " + indi["ID"] + ": US07: Over 150 years old"



def test_us08_birth_b4_marr_parents():
    #parse_to_objects(workFile)
    file = open("output.txt", "a")

    for indi in individuals_array:
        for fam in families_array:
            result = us08_birth_b4_marr_parents(indi,fam)
            if(result == -1):
                file.write("Error: Individual: " + indi["ID"] + ": US08: born after marriage of parents" + "\n")
                return "Error: Individual: " + indi["ID"] + ": US08: born after marriage of parents"
            elif(result == 0):
                file.write("born more than 9 months after divorce" + "\n")
                return "born more than 9 months after divorce"



def test_us09_birth_b4_death_parents():
    #parse_to_objects(workFile)
    file = open("output.txt", "a")
    for indi in individuals_array:
        for fam in families_array:
            result = us09_birth_b4_death_parents(indi,fam,individuals_array)
            if(result == 0):
                file.write("Error: Individual: " + indi["ID"] + ": US09 born after death of mom" + "\n")
                return "Error: Individual: " + indi["ID"] + ": US09 born after death of mom"
            elif(result == 1):
                file.write("Error: Individual: " + indi["ID"] + ": US09 born 9 months after death of dad" + "\n")
                return "Error: Individual: " + indi["ID"] + ": US09 born 9 months after death of dad"

def test_us_10_marriage_after_14():
    file = open("output.txt", "a")
    for fam in families_array:
        result = us_10_marriage_after_14(fam)
        if(result == False):
            #print("Error: Family: " + fam["ID"] + ": US10: Individuals were married before both were 14" + "\n")
            file.write("Error: Family: " + fam["ID"] + ": US10: Individuals were married before both were 14" + "\n")
            return "Error: Family: " + fam["ID"] + ": US10: Individuals were married before both were 14"

def test_us_11_no_bigamy():
    file = open("output.txt", "a")
    for indi in individuals_array:
        result = us_11_no_bigamy(indi)
        if(result == False):
            #print("Error: Individual: " + indi["ID"] + ": US11: Individual is married to multiple people" + "\n")
            file.write("Error: Individual: " + indi["ID"] + ": US11: Individual is married to multiple people" + "\n")
            return "Error: Individual: " + indi["ID"] + ": US11: Individual is married to multiple people"

def test_us12_parents_not_too_old():
    file = open("output.txt", "a")
    for indi in individuals_array:
        for fam in families_array:
            result = us12_parents_not_too_old(fam, indi)
            if(result == False):
                file.write("Error: Family: " + fam["ID"] + ": US12: Parents are too old" + "\n")
                return "Error: Family: " + fam["ID"] + ": US12: Parents are too old"

def test_us13_siblings_spacing():
    file = open("output.txt", "a")

    for indi in individuals_array:
        for fam in families_array:
            result = us13_siblings_spacing(fam, indi)
            if(result == False):
                file.write("Error: Family: " + fam["ID"] + ": US13: Siblings too close in age" + "\n")
                return "Error: Family: " + fam["ID"] + ": US13: Siblings too close in age"

def test_us14_multiple_births_lessthan_5():
    file = open("output.txt", "a")
    for fam in families_array:
        result = us14_multiple_births_lessthan_5(fam,individuals_array)
        if(result == False):
            file.write("Error: Family: " + fam["ID"] + ": US14 has more than 5 children with the same birth" + "\n")
            return "Error: Family: " + fam["ID"] + ": US14 has more than 5 children with the same birth"

def test_us15_fewer_than_15_siblings():
    file = open("output.txt", "a")
    for fam in families_array:
        result = us15_fewer_than_15_siblings(fam)
        if(result == False):
            file.write("Error: Family: " + fam["ID"] + ": US15 has 15 or more children" + "\n")
            return "Error: Family: " + fam["ID"] + ": US15 has 15 or more children"

def test_us16_male_last_names():
    file = open("output.txt", "a")
    for fam in families_array:
        print(fam)
        result = us16_male_last_names(fam)
        if(result == False):
            file.write("Error: Family: " + fam["ID"] + ": US16 has inconsistant male last name\n")
            return "Error: Family: " + fam["ID"] + ": US16 has inconsistant male last name"

def test_us17_no_marriages_to_children():
    file = open("output.txt", "a")
    for fam in families_array:
        result = us17_no_marriages_to_children(fam)
        if result == False:
            file.write("Error: Family " + fam["ID"] + ": US17: Parent can't marry child\n")
            return "Error: Family " + fam["ID"] + ": US17: Parent is married to child"

def test_us18_siblings_should_not_marry():
  file = open("output.txt", "a")
  for indi in individuals_array:
      result = us18_siblings_should_not_marry(indi)
      if result == False:
          file.write("Error: Indi: " + indi["ID"] + ": US18: Siblings can't be married" + "\n")
          return "Error: Indi: " + indi["ID"] + ": US18: Siblings can't be married"

def test_us19_first_cousins_should_not_marry():
    file = open("output.txt", "a")
    for indi in individuals_array:
        for indi2 in individuals_array:
            result = us19_first_cousins_should_not_marry(indi["ID"], indi2["ID"])
            if result == False:
                file.write("Error: Indi: " + indi["ID"] + indi2["ID"] + ": US19: First cousins should not marry\n")
                return "Error: Indi: " + indi["ID"] + indi2["ID"] + ": US19: First cousins should not marry"


def test_us21_correct_gender_role():
    file = open("output.txt", "a")

    for fam in families_array:
        result = us21_correct_gender_role(fam)
        if result == 0:
            file.write("Error: Family: " + fam["ID"] + ": US21: Wife is wrong gender" + "\n")
            return "Error: Family: " + fam["ID"] + ": US21: Wife is wrong gender"
        elif result == -1:
            file.write("Error: Family: " + fam["ID"] + ": US21: Husband is wrong gender" + "\n")
            return "Error: Family: " + fam["ID"] + ": US21: Husband is wrong gender"


def test_us22_unique_IDs():
    file = open("output.txt", "a+")
    result = us22_unique_IDs(id_match, famid_match)
    if result == 1:
        file.write("Error: Individual: US22: Duplicate ID number" + "\n")
        return "Error: Individual: US22: Duplicate ID number"
    if result == 0:
        file.write("Error: Family: US22: Duplicate ID number" + "\n")
        return "Error: Family: US22: Duplicate ID number"

def test_us23_unique_name_and_birth_date():
    file = open("output.txt", "a")
    errors = []
    for indi in individuals_array:
        result = us23_unique_name_and_birth_date(indi,individuals_array)
        if(result == False):
            file.write("Error: Individual: " + indi["ID"] + ": US23: Does not have a unique name and birthday" + "\n")
            errors.append("Error: Individual: " + indi["ID"] + ": US23: Does not have a unique name and birthday")
    return errors

def test_us24_unique_families_by_spouses():
    file = open("output.txt", "a")
    errors = []
    for fam in families_array:
        result = us24_unique_families_by_spouses(fam,families_array)
        if(result == False):
            file.write("Error: Family: " + fam["ID"] + ": US24: Does not have a unique husband, wife, and marriage date" + "\n")
            errors.append("Error: Family: " + fam["ID"] + ": US24: Does not have a unique husband, wife, and marriage date")
    return errors

def test_us25_unique_first_names_in_families():
    file = open("output.txt", "a")
    errors = []
    for fam in families_array:
        result = us25_unique_first_names_in_families(fam)
        print(result)
        if result == False:
            file.write("Error: Family: " + fam["ID"] + ": US25: Does not have unique sibling names and birthdays")
            errors.append("Error: Family: " + fam["ID"] + ": US25: Does not have unique sibling names and birthdays")
    return errors

def test_us26_corresponding_entries():
    file = open("output.txt", "a")
    for fam in families_array:
        for indi in individuals_array:
            result = us26_corresponding_entries(indi, fam)
            if result == False:
                file.write("Error Individual:" + indi["ID"] + " US26 individual table and family table do not match\n" )
                return "Error Individual:" + indi["ID"] + " US26 individual table and family table do not match"

def test_us27_include_individual_ages():
    file = open("output.txt", "a")
    for indi in individuals_array:
        result = us27_include_individual_ages(indi)
        file.write("US27: Include individual ages: " + indi["ID"] + " " + str(result) + "\n")
    return "US27: Include individual ages: " + indi["ID"] + " " + str(result)

def test_us28_order_siblings_by_age():
    file = open("output.txt", "a")
    for fam in families_array:
        result = us28_order_siblings_by_age(fam)
        file.write("US28: Order siblings from oldest to youngest: " + fam["ID"] + " " + str(result) + "\n")
    return "US28: Order siblings from oldest to youngest: " + fam["ID"] + " " + str(result)

def test_us29_list_deceased():
    file = open("output.txt", "a")

    result = us29_list_deceased(individuals_array)
    file.write("US29: List of all deaths in tree: " + str(result) + "\n")
    return "US29: List of all deaths in tree: " + str(result)

def test_us33_list_orphans():
    file = open("output.txt", "a")

    result = us33_list_orphans(individuals_array,families_array)
    file.write("US33: List of all orphans: " + str(result) + "\n")
    return "US33: List of all orphans: " + str(result)

def test_us35_list_recent_births():
    file = open("output.txt", "a")

    for indi in individuals_array:
        result = us35_list_recent_births(individuals_array)
        file.write("US35: List of all individuals born within the last 30 days: " + str(result) + "\n")
        return "US35: List of all individuals born within the last 30 days: " + str(result)

def test_us36_list_recent_deaths():
    file = open("output.txt", "a")

    for indi in individuals_array:
        result = us36_list_recent_deaths(individuals_array)
        file.write("US36: List of all individuals who died within the last 30 days: " + str(result) + "\n")
        return "US36: List of all individuals who died within the last 30 days: " + str(result)



def test_us38_list_upcoming_birthdays():
    file = open("output.txt", "a")
    for indi in individuals_array:
        result = us38_list_upcoming_birthdays(individuals_array)
        file.write("US38: List of all individuals whose birthdays are in the next 30 days: " + str(result) + "\n")
        return "US38: List of all individuals whose birthdays are in the next 30 days: " + str(result)


def test_validate_to_array():
    print(validate_to_array(workFile))



def test_parse_to_chart():
    print(parse_to_chart())
    with open("output.txt", "w+") as tables:
        tables.write(str(individual_table))
        tables.write(str(family_table))
        #tables.close()
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

#print(id_match)
#print(famid_match)
#test_parse_to_chart()
#parse_to_chart(workFile)
#print(individuals_array)


## TESTS
# print(test_us02_birth_b4_marriage())
# print(test_us03_birth_b4_death())


# print(test_us04_marr_b4_divorce())

# print(test_us05_marr_b4_death())
# print(test_us06_div_b4_death())
# print(test_us07_less_than_150())
# print(test_us08_birth_b4_marr_parents())
# print(test_us09_birth_b4_death_parents())

# print(test_us_10_marriage_after_14())
# print(test_us_11_no_bigamy())



# print(test_us12_parents_not_too_old())
# print(test_us13_siblings_spacing())
# print(test_us14_multiple_births_lessthan_5())
# print(test_us15_fewer_than_15_siblings())


# print(test_us21_correct_gender_role())
# print(test_us22_unique_IDs())
# print(test_us29_list_deceased())

# print(test_us35_list_recent_births())
# print(test_us36_list_recent_deaths())
# print(test_us38_list_upcoming_birthdays())



#print(datetime.today() + timedelta(days=30))



# END TESTS


# #test_validate_to_array()


# validate_to_array(workFile)

#test_parse_to_objects()
#us16_male_last_names(families_array[0])
#us16_male_last_names(families_array[2])
#print(test_us16_male_last_names())

#print(us19_first_cousins_should_not_marry(individuals_array[0]["ID"], individuals_array[10]["ID"]))
#print(test_us19_first_cousins_should_not_marry())
#print(test_us25_unique_first_names_in_families())
