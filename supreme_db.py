import sqlite3
import os

DATABASE_FILE = "Pizza_database.db"
faction_conversion = {
    "A": "Aeon",
    "E": "UEF",
    "R": "Cybran",
    "S": "Seraphim"
}
units_path = "S:/units"


#cursor = connection.cursor()
#sql = f"SELECT * FROM {table}"
#cursor.execute(sql) #executes the SELECT statement on the chosen table
#results = cursor.fetchall() #stores the results in the results variable


#with sqlite3.connect(DATABASE_FILE) as connection:
#    pass




def get_name_from_line(line):
    '''gets unit name from line with syntax:     Description = "<LOC uaa0101_desc>Air Scout",'''
    start_appending = False
    output = ""
    for i in line:
        if start_appending and i == '"':
            return output
        if start_appending:
            output = output + i
        if i == ">":
            start_appending = True


def get_category_from_line(line):
    start_appending = False
    output = ""
    for i in line:
        if start_appending and i == ' ':
            return output
        if i != " ":
            start_appending = True
        if start_appending:
            output = output + i


def get_number_from_line(line):
    output = ""
    for i in line:
        if i.isdigit():
            output = output + i
    return int(output)


def iterate_through_file():
    ''' loops through unit blueprint and extracts and sets all required variables out'''
    line_number = 0
    for line in unit_blueprint:
        if line_number == 1:
            unit_name = get_name_from_line(line)
        
        if "= {" in line and "    " in line and "     " not in line: #detects for beginnings of a second level dictionary
            current_section = get_category_from_line(line)
        
        if current_section == "Categories":
            if '"AIR"' in line:
                roles["Air"] = True
            if '"NAVAL"' in line:
                roles["Naval"] = True
            if '"LAND"' in line:
                roles["Land"] = True
            if '"AMPHIBIOUS"' in line:
                roles["Land"] = True
                roles["Naval"] = True
            if '"ANTIAIR"' in line:
                roles["Anti Air"] = True
            if '"ANTINAVY"' in line:
                roles["Anti Naval"] = True
            
        if current_section == "Defense":
            if ' Health = ' in line:
                unit_health = get_number_from_line(line)
        
        if current_section == "Economy":
            if ' BuildCostEnergy =' in line:
                unit_energy_cost = get_number_from_line(line)
            if ' BuildCostMass =' in line:
                unit_mass_cost = get_number_from_line(line)
            if ' BuildTime =' in line:
                unit_build_time = get_number_from_line(line)


def add_unit_to_supreme_database():
    pass


def process_file(filename):
    #UAA0101 [0] is unit  [1] is faction   [2] is unit type  [4] is tech level

    #filters out non units and civilians and buildings
    if len(filename) != 7:
        return
    if filename[0] != "U" and filename[0] != "X":
        return
    if filename[2] == "C" or filename[2] == "B":
        return
    print(filename)
    return

    #initialise variables
    text_file = open('H:/13DTP/SupremeDatabase/Units/UAA0101_unit.bp','r')
    unit_blueprint = text_file.readlines()
    current_section = ""
    unit_name = ""
    unit_health = 0
    unit_tech_level = int(filename[4])
    unit_faction = faction_conversion[filename[1]]
    unit_mass_cost = 0
    unit_energy_cost = 0
    unit_build_time = 0
    roles = {
        "Air": False,
        "Naval": False,
        "Land": False,
        "Anti Air": False,
        "Anti Naval": False
    }

    iterate_through_file()

    add_unit_to_supreme_database()

            



for filename in os.listdir(units_path):
    process_file(filename)
