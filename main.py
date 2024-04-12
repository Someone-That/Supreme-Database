import sqlite3


DATABASE_FILE = "supreme_db.db"


class unit:  # initialise variables
    identification = 0
    name = ""
    health = 0
    tech_level = 0
    faction = "nothing"
    mass_cost = 0
    energy_cost = 0
    build_time = 0
    roles = []


'''Functions'''


def sql_statement(connection, sql):
    '''executes sql statement'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except:
        return


def show_units(connection, id_filter=0, disable_sort=False, tech_filter=[1, 2, 3, 4], faction_filter=["Seraphim", "UEF", "Cybran", "Aeon"], role_filter=["Land", "Air", "Naval", "Anti Air", "Anti Naval"]):
    '''constructs sql statement with filters then nicely prints out units'''
    try:
        # example filter: WHERE (role_name = "Anti Naval" OR role_name = "Anti Air") AND (tech_level = 1 OR tech_level = 2) AND (faction_name = "Aeon" OR faction_name = "UEF")
        rf = ""
        for i in range(len(role_filter)):
            rf = rf + f"role_name = '{role_filter[i]}'"
            if i < len(role_filter)-1:
                rf = rf + " OR "

        tf = ""
        for i in range(len(tech_filter)):
            tf = tf + f"tech_level = {tech_filter[i]}"
            if i < len(tech_filter)-1:
                tf = tf + " OR "

        ff = ""
        for i in range(len(faction_filter)):
            ff = ff + f"faction_name = '{faction_filter[i]}'"
            if i < len(faction_filter)-1:
                ff = ff + " OR "

        filter = f"WHERE ({rf}) AND ({tf}) AND ({ff})"
        if id_filter:
            filter = filter + f" AND id = {id_filter}"
        
        order = "ORDER BY faction_name, tech_level"
        if disable_sort:
            order = ""
        sql = f"""
SELECT id, name, health, mass_cost, energy_cost, build_time, tech_level, faction_name FROM
Units JOIN Unit_Roles ON Units.id = Unit_Roles.uid
JOIN Roles ON Roles.role_id = Unit_Roles.rid
JOIN Factions ON fid = faction_id
{filter}
GROUP BY id
{order}"""

        results = sql_statement(connection, sql)
        if not results:
            print("\nNo results found.")
            return
        print(f"\n{'id':<5}{'Name':<42}{'Health':<15}{'Mass Cost':<15}{'Energy Cost':<15}{'Build Time':<15}{'Tech Level':<15}{'Faction':<10}")  # print out the column headings with spacing
        for item in results:
            print(f"{item[0]:<5}{item[1]:<42}{item[2]:<15}{item[3]:<15}{item[4]:<15}{item[5]:<15}{item[6]:<15}{item[7]:<10}")
    except:
        print("\nSomething went wrong with connection.")


def spacing(spacing: int = 60):
    '''prints 60 new lines'''
    print("\n" * spacing)


def ask_user_for_number(lowest_choice, highest_choice):
    '''bullet proof function that asks the user for a number and only accepts a number within the parameters'''
    while True:
        try:  # asks the user for an integer and responds appropriately
            user_answer = int(input("\nTo pick an option, type a number: "))
            if user_answer < lowest_choice or user_answer > highest_choice:
                print("\nThat is not an option.")
                # print("\nYour life is NOTHING. You serve ZERO purpose. You should retry NOW.")
            else:
                return user_answer
        except ValueError:  # the user failed to type in an integer
            print("\nThat is not an integer.")
            # print("\nYour life is NOTHING. You serve ZERO purpose. You should retry NOW.")


def ask_user_for_number_list(lowest_choice, highest_choice):
    '''bullet proof function that asks the user for a list of numbers and only accepts valid inputs'''
    while True:
        return_list = set()
        user_answer = input("\nNumbers: ")
        broke = False
        for i in user_answer:
            if i.isdigit():
                i = int(i)
                if i < lowest_choice or i > highest_choice:
                    # print("\nOut of range number/s and worthless life detected. You serve ZERO purpose. You should retry NOW.")
                    print("\nOut of range number/s detected.")
                    broke = True
                    break
                else:
                    return_list.add(i)
        if broke:
            continue
        if return_list:
            return_list = sorted(list(return_list))

            if highest_choice in return_list:  # user selected the 'all' option
                return_list = []
                for i in range(highest_choice-1):
                    return_list.append(i+1)

            return return_list

        # user inputted no numbers
        # print("\nNo numbers detected, input numbers. Your life is NOTHING. You serve ZERO purpose. You should retry NOW.")
        print("\nNo numbers detected, input numbers.")


def convert_numbers_to_corresponding_list(list, numbers):
    return_list = []
    for i in numbers:
        return_list.append(list[i-1])
    return return_list


def pause():
    input("\nEnter to continue: ")


def user_show_units(connection):
    '''will take the user through the process of showing units'''

    # go through filtering process
    print("\nType the numbers of the tech levels you would like to filter for: ")
    print("""
        1. Tech level 1
        2. Tech level 2
        3. Tech level 3
        4. Experimental (Tech level 4)
        5. All tech levels

E.G. To select tech levels 1 and 2, type '1, 2' or '1 2' or '12'""")
    tech_levels_to_filter_for = ask_user_for_number_list(1, 5)

    print("\nType the numbers of the factions you would like to filter for: ")
    print("""
        1. Seraphim
        2. UEF
        3. Cybran
        4. Aeon
        5. All factions

E.G. To select factions Seraphim and UEF, type '1, 2' or '1 2' or '12'""")
    factions_to_filter_for = ask_user_for_number_list(1, 5)
    factions = ["Seraphim", "UEF", "Cybran", "Aeon"]
    factions_to_filter_for = convert_numbers_to_corresponding_list(factions, factions_to_filter_for)

    print("\nType the numbers of the roles you would like to filter for: ")
    print("""
        1. Land
        2. Air
        3. Navy
        4. Anti-Air
        5. Anti-Navy
        6. All roles

E.G. To select roles Land and Air, type '1, 2' or '1 2' or '12'""")
    roles_to_filter_for = ask_user_for_number_list(1, 6)
    roles = ["Land", "Air", "Naval", "Anti Air", "Anti Naval"]
    roles_to_filter_for = convert_numbers_to_corresponding_list(roles, roles_to_filter_for)

    show_units(connection, 0, False, tech_levels_to_filter_for, factions_to_filter_for, roles_to_filter_for)
    pause()


def ask_user_for_unit(connection, intent):
    '''displays all units then asks user for the id of one'''
    show_units(connection, 0, True)
    print(f"\nType the id of the unit you would like to {intent}.")
    while True:
        unit_id = ask_user_for_number(0, 9999999)
        if sql_statement(connection, f"SELECT name FROM Units WHERE id = {unit_id}"):  # if this returns something it means id was valid
            return unit_id
        else:
            print("\nID doesn't belong to any unit. Try again.")


def ask_user_for_text(max_length):
    while True:
        output = input("\nInput: ")
        if len(output) > max_length or len(output) < 3:
            print("\nInvalid output length.")
            continue
        if output.isdigit():
            print("\nInvalid input.")
            continue
        return output


def add_unit_to_supreme_database(connection):
    cursor = connection.cursor()

    faction_id = unit.faction

    #  insert unit data
    sql = f"INSERT INTO Units VALUES ({unit.identification}, '{unit.name}', {unit.health}, {unit.mass_cost}, {unit.energy_cost}, {unit.build_time}, {unit.tech_level}, {faction_id});"

    cursor.execute(sql)

    #  insert unit roles
    for role in unit.roles:
        #  get role id
        sql = f"SELECT role_id FROM Roles WHERE role_name = '{role}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        role_id = results[0][0]

        #  insert unit into role
        sql = f"INSERT INTO Unit_Roles VALUES ({unit.identification}, {role_id});"
        cursor.execute(sql)


def delete_unit_from_supreme_database(connection, id):
    sql_statement(connection, f"DELETE FROM Units WHERE id = {id};")
    sql_statement(connection, f"DELETE FROM Unit_Roles WHERE uid = {id};")


def user_update_unit(connection):
    '''will take the user through the process of updating units'''
    unit.identification = ask_user_for_unit(connection, "update")

    show_units(connection, unit.identification)
    print("\nType the new name you would like for this unit.")
    unit.name = ask_user_for_text(40)

    show_units(connection, unit.identification)
    print("\nType the new health value you would like for this unit.")
    unit.health = ask_user_for_number(1, 999999)

    show_units(connection, unit.identification)
    print("\nType the new mass cost value you would like for this unit.")
    unit.mass_cost = ask_user_for_number(1, 999999)

    show_units(connection, unit.identification)
    print("\nType the new energy cost value you would like for this unit.")
    unit.energy_cost = ask_user_for_number(1, 999999)

    show_units(connection, unit.identification)
    print("\nType the new build time value you would like for this unit.")
    unit.build_time = ask_user_for_number(1, 999999)

    show_units(connection, unit.identification)
    print("\nType the new tech level you would like for this unit (from 1 to 4).")
    unit.tech_level = ask_user_for_number(1, 4)

    show_units(connection, unit.identification)
    print("\nType the number of the new faction you would like for this unit.")
    print("""
        1. Seraphim
        2. Cybran
        3. Aeon
        4. UEF""")
    unit.faction = ask_user_for_number(1, 4)

    print("\nType the numbers of the roles you would like for this unit: ")
    print("""
        1. Land
        2. Air
        3. Navy
        4. Anti-Air
        5. Anti-Navy
        6. All roles

E.G. To select roles Land and Air, type '1, 2' or '1 2' or '12'""")
    unit.roles = ask_user_for_number_list(1, 6)
    roles = ["Land", "Air", "Naval", "Anti Air", "Anti Naval"]
    unit.roles = convert_numbers_to_corresponding_list(roles, unit.roles)

    delete_unit_from_supreme_database(connection, unit.identification)
    add_unit_to_supreme_database(connection)
    print("\nYour updated unit:")
    show_units(connection, unit.identification)
    pause()


def user_add_unit(connection):
    '''will take the user through the process of adding units'''
    # assign unit id
    all_ids = sql_statement(connection, "SELECT id from Units")
    highest_id = 1
    for id in all_ids:
        if id[0] > highest_id:
            highest_id = id[0]
    highest_id += 1
    unit.identification = highest_id

    print("\nType the name you would like for this unit.")
    unit.name = ask_user_for_text(40)

    print("\nType the health value you would like for this unit.")
    unit.health = ask_user_for_number(1, 999999)

    print("\nType the mass cost value you would like for this unit.")
    unit.mass_cost = ask_user_for_number(1, 999999)

    print("\nType the energy cost value you would like for this unit.")
    unit.energy_cost = ask_user_for_number(1, 999999)

    print("\nType the build time value you would like for this unit.")
    unit.build_time = ask_user_for_number(1, 999999)

    print("\nType the tech level you would like for this unit (from 1 to 4).")
    unit.tech_level = ask_user_for_number(1, 4)

    print("\nType the number of the faction you would like for this unit.")
    print("""
        1. Seraphim
        2. Cybran
        3. Aeon
        4. UEF""")
    unit.faction = ask_user_for_number(1, 4)

    print("\nType the numbers of the roles you would like for this unit: ")
    print("""
        1. Land
        2. Air
        3. Navy
        4. Anti-Air
        5. Anti-Navy
        6. All roles

E.G. To select roles Land and Air, type '1, 2' or '1 2' or '12'""")
    unit.roles = ask_user_for_number_list(1, 6)
    roles = ["Land", "Air", "Naval", "Anti Air", "Anti Naval"]
    unit.roles = convert_numbers_to_corresponding_list(roles, unit.roles)

    add_unit_to_supreme_database(connection)
    print("\nYour new unit:")
    show_units(connection, unit.identification)
    pause()


def user_delete_unit(connection):
    '''will take the user through the process of deleting units'''
    unit.identification = ask_user_for_unit(connection, "delete")
    delete_unit_from_supreme_database(connection, unit.identification)
    print("\nUnit's existence successfully terminated.")
    pause()


# code below here handles the console interfacing
def console_interface(connection):
    spacing()
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
