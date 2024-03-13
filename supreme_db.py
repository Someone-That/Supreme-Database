import sqlite3

DATABASE_FILE = "Pizza_database.db"


#cursor = connection.cursor()
#sql = f"SELECT * FROM {table}"
#cursor.execute(sql) #executes the SELECT statement on the chosen table
#results = cursor.fetchall() #stores the results in the results variable


#with sqlite3.connect(DATABASE_FILE) as connection:
#    pass

text_file = open('H:/13DTP/SupremeDatabase/Units/UAA0101_unit.bp','r')
unit_blueprint = text_file.readlines()
current_section = ""
roles = {
    "Air": False,
    "Naval": False,
    "Land": False,
    "Anti Air": False,
    "Anti Naval": False
}


for line in unit_blueprint:
    if "Categories" in line:
        current_section = "categories"
    
    if "= {" in line and "    " in line and "     " not in line: #detects for starting of a second level dictionary
        current_section = line
    if current_section == "categories":
        if '"AIR"' in line:
            pass
            #print(line)

