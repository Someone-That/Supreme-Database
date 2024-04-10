import sqlite3


DATABASE_FILE = "supreme_db.db"


'''Functions'''


def sql_statement(connection, sql):
    '''executes sql statement'''
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


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


def spacing(spacing: int = 60):
    '''prints 60 new lines'''
    for nothing in range(spacing):
        print("\n")


def ask_user_for_number(lowest_choice, highest_choice):
    '''bullet proof function that asks the user for a number and only accepts a number within the parameters'''
    while True:
        try:  # asks the user for an integer and responds appropriately
            print("")
            user_answer = int(input("To pick an option, type a number: "))
            if user_answer < lowest_choice or user_answer > highest_choice:
                print("")
                #print("That is not an option.")
                print("Your life is NOTHING. You serve ZERO purpose. You should retry NOW.")
            else:
                return user_answer
        except ValueError:  # the user failed to type in an integer
            print("")
            #print("That is not an integer.")
            print("Your life is NOTHING. You serve ZERO purpose. You should retry NOW.")


def ask_user_for_number_list(lowest_choice, highest_choice):
    '''bullet proof function that asks the user for a list of numbers and only accepts valid inputs'''
    while True:
        try:  # asks the user for an integer and responds appropriately
            print("")
            user_answer = int(input("To pick an option, type a number: "))
            if user_answer < lowest_choice or user_answer > highest_choice:
                print("")
                #print("That is not an option.")
                print("Your life is NOTHING. You serve ZERO purpose. You should retry NOW.")
            else:
                return user_answer
        except ValueError:  # the user failed to type in an integer
            print("")
            #print("That is not an integer.")
            print("Your life is NOTHING. You serve ZERO purpose. You should retry NOW.")


def user_show_units(connection):
    '''will take the user through the process of showing units'''

    # go through filtering process
    print("\nType the numbers of the tech levels you would like to filter for:")
    print("""
        1. Tech level 1
        2. Tech level 2
        3. Tech level 3
        4. Experimental (Tech level 4)
        5. All tech levels
E.G. To select tech levels 1 and 2, type '1, 2' or '1 2'""")
    tech_levels_to_filter_for = []
    
    print("What faction would you like to filter for?")
    print("""
        1. Seraphim
        2. UEF
        3. Cybran
        4. Aeon
        5. All factions""")


def user_update_unit(connection):
    #show units
    #unit_id_to_update = ask_user_for_number(1,max)
    pass


def user_add_unit(connection):
    pass


def user_delete_unit(connection):
    #show units
    #unit_to_delete = ask_user_for_number(1, max)
    sql_statement(connection)


# code below here handles the console interfacing
def console_interface(connection):
    #spacing()
    print("What would you like to do?")
    print("""
        1. Show units
        2. Update a unit
        3. Add a unit
        4. Delete a unit""")
    what_to_do = ask_user_for_number(1, 4)  # asks the user what they'd like to do

    match what_to_do:
        case 1:  # user wants to see units
            user_show_units(connection)
        case 2:  # user wants to update a unit
            user_update_unit(connection)
        case 3:  # user wants to add a unit
            user_add_unit(connection)
        case 4:  # user wants to delete a unit
            user_delete_unit(connection)


with sqlite3.connect(DATABASE_FILE) as connection:
    while True:
        console_interface(connection)
    # cursor = connection.cursor()
    # sql = "SELECT Units.name, Roles.name FROM Unit_Roles JOIN Units ON Unit_Roles.uid = Units.id JOIN Roles ON Unit_Roles.rid = Roles.id"
    # cursor.execute(sql) #executes the SELECT statement on the chosen table
    # results = cursor.fetchall() #stores the results in the results variable
    # print(results)
