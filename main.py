import sqlite3


DATABASE_FILE = "supreme_db.db"


'''Functions'''


def display_results(connection, sql):
    '''nicely print out a table'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()  # stores the results in the results variable
        print(f"\n{'id':<5}{'Topping Name':<20}{'Price':<60}")  # print out the column headings with spacing
        for item in results: #prints out the items of the pizza toppings table with the same spacing as the headings
            id += 1
            print(f"{item[0]:<5}{item[1]:<20}{item[2]:<60}")
    except:
        print("Something went wrong with connection.")


def spacing(): 
    '''prints 60 new lines'''
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


with sqlite3.connect(DATABASE_FILE) as connection:
    cursor = connection.cursor()
    sql = "SELECT Units.name, Roles.name FROM Unit_Roles JOIN Units ON Unit_Roles.uid = Units.id JOIN Roles ON Unit_Roles.rid = Roles.id"
    cursor.execute(sql) #executes the SELECT statement on the chosen table
    results = cursor.fetchall() #stores the results in the results variable
    print(results)