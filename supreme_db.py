import sqlite3
import os

DATABASE_FILE = "Pizza_database.db"
faction_conversion = {
    "A": "Aeon",
    "E": "UEF",
    "R": "Cybran",
    "S": "Seraphim"
}
units_path = "S:/units/"


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
    for line in unit.blueprint:
        if line_number == 1:
            unit.name = get_name_from_line(line)
        
        if "= {" in line and "    " in line and "     " not in line:  # detects for beginnings of a second level dictionary
            unit.current_section = get_category_from_line(line)
        
        if unit.current_section == "Categories":
            if '"AIR"' in line:
                unit.roles["Air"] = True
            if '"NAVAL"' in line:
                unit.roles["Naval"] = True
            if '"LAND"' in line:
                unit.roles["Land"] = True
            if '"AMPHIBIOUS"' in line:
                unit.roles["Land"] = True
                unit.roles["Naval"] = True
            if '"ANTIAIR"' in line:
                unit.roles["Anti Air"] = True
            if '"ANTINAVY"' in line:
                unit.roles["Anti Naval"] = True
            
        if unit.current_section == "Defense":
            if ' Health = ' in line:
                unit.health = get_number_from_line(line)
        
        if unit.current_section == "Economy":
            if ' BuildCostEnergy =' in line:
                unit.energy_cost = get_number_from_line(line)
            if ' BuildCostMass =' in line:
                unit.mass_cost = get_number_from_line(line)
            if ' BuildTime =' in line:
                unit.build_time = get_number_from_line(line)
        line_number += 1


def add_unit_to_supreme_database():
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        sql = f"SELECT * FROM {table}"
        cursor.execute(sql) #executes the SELECT statement on the chosen table


def process_file(filename):
    # UAA0101 [0] is unit  [1] is faction   [2] is unit type  [4] is tech level

    # filters out non units and civilians and buildings
    if len(filename) != 7:
        return
    if filename[0] != "U" and filename[0] != "X":
        return
    if filename[2] == "C" or filename[2] == "B":
        return
    if filename[1] == "X":
        return

    # initialise variables
    unit.blueprint = ""
    try:
        text_file = open(f"{units_path}{filename}/{filename}_unit.bp", 'r')
        unit.blueprint = text_file.readlines()
    except:  # unacceptable file pattern detected
        return
    unit.current_section = ""
    unit.name = ""
    unit.health = 0
    unit.tech_level = int(filename[4])
    unit.faction = faction_conversion[filename[1]]
    unit.mass_cost = 0
    unit.energy_cost = 0
    unit.build_time = 0
    unit.roles = {
        "Air": False,
        "Naval": False,
        "Land": False,
        "Anti Air": False,
        "Anti Naval": False
    }


    iterate_through_file()
    if unit.roles["Anti Air"] and unit.roles["Land"]:
        print(unit.name, unit.health, unit.faction, unit.mass_cost, unit.energy_cost, unit.build_time)
    return

    add_unit_to_supreme_database()

            


#initialise variables
class unit:
    blueprint = ""
    current_section = ""
    name = ""
    health = 0
    tech_level = 0
    faction = "nothing"
    mass_cost = 0
    energy_cost = 0
    build_time = 0
    roles = {
        "Air": False,
        "Naval": False,
        "Land": False,
        "Anti Air": False,
        "Anti Naval": False
    }
for filename in os.listdir(units_path):
    process_file(filename)
