import unittest
from gedcom_parser import families_array, individuals_array
import gedcom_parser

# class TestStringMethods(unittest.TestCase):
#     def test1(self):
#         # This test is only true when using the test.ged file 
#         self.assertEqual(gedcom_parser.test_us04_marr_b4_divorce(), "Error: Family: @F3@: US04: Divorced 3 FEB 1995 before married 6 AUG 1995")
#         print("Error: Family: @F3@: US04: Divorced 3 FEB 1995 before married 6 AUG 1995")

# if __name__ == '__main__':
#     unittest.main()



fname = input("Enter file name: ")

workFile = open(fname)

def test_us02_birth_b4_marriage():
    gedcom_parser.parse_to_objects(workFile)
    file = open("output.txt", "w+")
    for fam in families_array:
        result = gedcom_parser.us02_birth_b4_marriage(fam)
        if result == False:
             file.write("Error: Family: " + fam["ID"] +  ": US02: Birthday before married " + fam["Married"] + "\n")
             return "Error: Family: " + fam["ID"] +  ": US02: Birthday before married " + fam["Married"]
    
    #file.close()

def test_us03_birth_b4_death():
    gedcom_parser.parse_to_objects(workFile)
    file = open("output.txt", "a+")
    for indi in individuals_array:
        result = gedcom_parser.us03_birth_b4_death(indi)
        if result == False:
            file.write("Error: Indi: " + indi["ID"] + " US03: Death " + indi["Death"] + " before Birthday " + indi["Birthday"] + "\n")
            #return "Error: Indi: " + indi["ID"] + " US03: Death " + indi["Death"] + " before Birthday " + indi["Birthday"]
    #file.close()


def test_us04_marr_b4_divorce():
    gedcom_parser.parse_to_objects(workFile)
    file = open("output.txt", "a+")

    for fam in families_array:
        result = gedcom_parser.us04_marr_b4_divorce(fam)
        if result == False:
            file.write("Error: Family: " + fam["ID"] +  ": US04: Divorced " + fam["Divorced"] + " before married " + fam["Married"] + "\n")
            return "Error: Family: " + fam["ID"] +  ": US04: Divorced " + fam["Divorced"] + " before married " + fam["Married"]
    
    #file.close()

def test_us05_marr_b4_death():
    gedcom_parser.parse_to_objects(workFile)
    file = open("output.txt", "a+")

    for fam in families_array:
        result = gedcom_parser.us05_marr_b4_death(fam)
        if(result == -1):
            file.write("Error: Family: " + fam["ID"] + ": US05: Death of husband before married " + fam["Married"] + "\n")
            #return "Error: Family: " + fam["ID"] + ": US05: Death of husband before married " + fam["Married"]
        elif(result == 1):
            file.write("Error: Family: " + fam["ID"] + ": US05: Death of wife before married " + fam["Married"] + "\n")
            #return "Error: Family: " + fam["ID"] + ": US05: Death of wife before married " + fam["Married"]
    #file.close()

def test_us06_div_b4_death():
    gedcom_parser.parse_to_objects(workFile)
    file = open("output.txt", "a+")

    
    for fam in families_array: 
        result = gedcom_parser.us06_div_b4_death(fam)
        if(result == 1 or result == -1): 
            file.write("Error: Family: " + fam["ID"] + ": US06: Died before divorce " + fam["Divorced"] + "\n")
            #return "Error: Family: " + fam["ID"] + ": US06: Died " + fam["Death"] + " before divorce " + fam["Divorced"]
    #file.close()

def test_us07_less_than_150(): 
    gedcom_parser.parse_to_objects(workFile)
    file = open("output.txt", "a+")

    for indi in individuals_array: 
        result = gedcom_parser.us07_less_than_150(indi)
        if result == False: 
            file.write("Error: Individual: " + indi["ID"] + ": US07: Over 150 years old" + "\n")
            #return "Error: individual: " + indi["ID"] + ": US07: Over Age " + indi["Age"]
    


def test_us08_birth_b4_marr_parents():
    gedcom_parser.parse_to_objects(workFile)
    file = open("output.txt", "a+")

    for indi in individuals_array:
        for fam in families_array:
            result = gedcom_parser.us08_birth_b4_marr_parents(indi,fam)
            if(result == -1):
                file.write("Error: Individual: " + indi["ID"] + ": US08: born after marriage of parents" + "\n")
            elif(result == 0):
                file.write("born more than 9 months after divorce" + "\n")
   


def test_us09_birth_b4_death_parents():
    gedcom_parser.parse_to_objects(workFile)
    file = open("output.txt", "a+")
    for indi in individuals_array:
        for fam in families_array:
            result = gedcom_parser.us09_birth_b4_death_parents(indi,fam,individuals_array)
            if(result == 0):
                file.write("Error: Individual: " + indi["ID"] + ": US09 born after death of mom" + "\n")
            elif(result == 1):
                file.write("Error: Individual: " + indi["ID"] + ": US09 born 9 months after death of dad" + "\n")
    file.close()


test_us02_birth_b4_marriage()

test_us03_birth_b4_death()

test_us04_marr_b4_divorce()

test_us05_marr_b4_death()
test_us06_div_b4_death()

test_us07_less_than_150()

test_us08_birth_b4_marr_parents()

test_us09_birth_b4_death_parents()



# gedcom_parser.test_us02_birth_b4_marriage()

# gedcom_parser.test_us03_birth_b4_death()


# gedcom_parser.test_us04_marr_b4_divorce()

# gedcom_parser.test_us05_marr_b4_death()
# gedcom_parser.test_us06_div_b4_death()

# gedcom_parser.test_us07_less_than_150()

# gedcom_parser.test_us08_birth_b4_marr_parents()

# gedcom_parser.test_us09_birth_b4_death_parents()