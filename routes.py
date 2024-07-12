from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)
DATABASE_FILE = "supreme_db.db"
tech_filter = []
faction_filter = []
role_filter = []


button_order = ['1', '2', '3', '4', "UEF", "Aeon", "Cybran", "Seraphim", "Land", "Air", "Naval", "Anti Air", "Anti Naval"]
button_toggles = [False, False, False, False, False, False, False, False, False, False, False, False, False]


def sql_statement(sql):
    '''executes sql statement'''
    try:
        with sqlite3.connect(DATABASE_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
    except:
        return


def clean_up_data(data):
    '''this function converts all tuples with only a single item in a list into non tuples, this removes the need to type something like ids[0][0]'''
    clean_data = []
    for i in data:
        clean_data.append(i[0])
    return clean_data


def convert_button_toggles_to_css_class():
    return_output = []
    for toggle in button_toggles:
        if toggle:
            return_output.append("fb-on")
        else:
            return_output.append("fb-off")
    return return_output


def process_filter_button_pressed(data):
    '''adds or removes selected filter from the filter lists'''
    if data[0] == "T":
        if data[1] in tech_filter:
            tech_filter.remove(data[1])
        else:
            tech_filter.append(data[1])

    if data[0] == "F":
        if data[1:] in faction_filter:
            faction_filter.remove(data[1:])
        else:
            faction_filter.append(data[1:])

    if data[0] == "R":
        if data[1:] in role_filter:
            role_filter.remove(data[1:])
        else:
            role_filter.append(data[1:])

    # tracks which button was pressed so the site can know which css toggle state to use for that button
    all_filters = tech_filter + faction_filter + role_filter
    data = data[1:]
    if data in all_filters:  # filter is selected
        button_toggles[button_order.index(data)] = True
    else:  # filter is unselected
        button_toggles[button_order.index(data)] = False


def construct_filter_statement(faction_site=""):
    '''uses filter lists to construct an sql WHERE statement which will contain all filters selected'''
    tf = ""
    for i in range(len(tech_filter)):
        tf = tf + f"tech_level = {tech_filter[i]}"
        if i < len(tech_filter)-1:
            tf = tf + " OR "

    rf = ""
    for i in range(len(role_filter)):
        rf = rf + f"role_name = '{role_filter[i]}'"
        if i < len(role_filter)-1:
            rf = rf + " OR "

    if faction_site:
        ff = f"faction_name = '{faction_site}'"
    else:
        ff = ""
        for i in range(len(faction_filter)):
            ff = ff + f"faction_name = '{faction_filter[i]}'"
            if i < len(faction_filter)-1:
                ff = ff + " OR "

    if not rf and not tf and not ff:  # no filters selected
        return ""
    filter = "WHERE "
    count = 0
    filter_list = [rf, tf, ff]
    for i in filter_list:  # constructs the statement appropriately
        if not i:
            continue
        count += 1
        if count == 1:
            filter = filter + f"({i})"
        else:
            filter = filter + f" AND ({i})"

    return filter


def construct_unit_title(unit_id):
    unit = sql_statement(f"""
SELECT id, unit_name, tech_level, name, code FROM
Units JOIN Unit_Roles ON Units.id = Unit_Roles.uid
JOIN Roles ON Roles.role_id = Unit_Roles.rid
JOIN Factions ON fid = faction_id
WHERE id = {unit_id}
GROUP BY id""")
    unit = unit[0]
    # put units in digestable form for website output
    if unit[2] == 4 or unit[2] == 0:  # unit is experimental or doesn't have a tech level
        result = f"{unit[3]}"
    else:
        result = f"T{unit[2]} {unit[3]}"  # example output: T1 Engineer [UAL0105]
    if unit[1]:  # unit has a name
        result = f"{unit[1]}: {result}"
    result = f"{unit[0]}. {result}"
    return result


def validate_stat(min, max, type, stat):  # there are 4 types: text, number, personal name
    if type == "personal name":
        if sql_statement(f"SELECT name FROM Units WHERE unit_name = {stat}"):  # personal name is taken
            return "Unit's personal name already exists, choose another."

    if type == "number":
        try:
            int(stat)
        except ValueError:
            return "Number input needed."

    stat_length = len(stat)
    
    if stat_length == 0:
        return "Missing input."
    if stat_length < min:
        return "Too little characters."
    if stat_length > max:
        return "Too many characters."


def validate_unit(save_data):
    nt = {}
    nt["unit_name"] = validate_stat(2, 25, "text", save_data["unit_name"])
    nt["unit_health"] = validate_stat(1, 7, "number", save_data["unit_health"])
    nt["unit_mass_cost"] = validate_stat(1, 7, "number", save_data["unit_mass_cost"])
    nt["unit_energy_cost"] = validate_stat(1, 7, "number", save_data["unit_energy_cost"])
    nt["unit_build_time"] = validate_stat(1, 7, "number", save_data["unit_build_time"])
    nt["unit_code"] = validate_stat(7, 7, "text", save_data["unit_code"])
    nt["unit_unit_name"] = validate_stat(2, 25, "personal name", save_data["unit_unit_name"])

    has_role = False
    roles = ["Land", "Air", "Navy", "Anti Air", "Anti Naval"]
    for role in roles:
        if role in save_data:
            has_role = True
            break
    if not has_role:
        nt["unit_roles"] = "Missing input."
    
    return nt


def delete_unit_from_supreme_database(unit_id):
    sql_statement(f"DELETE FROM Units WHERE id = {unit_id};")
    sql_statement(f"DELETE FROM Unit_Roles WHERE uid = {unit_id};")


def add_unit_to_supreme_database(sd, do_not_create_new_id = False):  # sd = save_data
    # assign unit id
    if do_not_create_new_id:
        unit_id = do_not_create_new_id
    else:
        all_ids = sql_statement("SELECT id from Units")
        highest_id = 1
        for id in all_ids:
            if id[0] > highest_id:
                highest_id = id[0]
        highest_id += 1
        unit_id = highest_id

    #  insert unit data
    sql_statement(f"INSERT INTO Units VALUES ({unit_id}, '{sd['unit_name']}', {sd['unit_health']}, {sd['unit_mass_cost']}, {sd['unit_energy_cost']}, {sd['unit_build_time']}, {sd['unit_tech_level']}, {sd['unit_faction']}, '{sd['unit_code']}', '{sd['unit_unit_name']}');")

    #  insert unit roles
    unit_roles = []
    roles = ["Land", "Air", "Navy", "Anti Air", "Anti Naval"]
    for role in roles:
        if role in sd:
            unit_roles.append(role)

    for role in unit_roles:
        #  get role id
        results = sql_statement(f"SELECT role_id FROM Roles WHERE role_name = '{role}'")
        role_id = results[0][0]

        #  insert unit into role
        sql_statement(f"INSERT INTO Unit_Roles VALUES ({unit_id}, {role_id});")


@app.route('/')
def home():
    extraction = sql_statement(f"""
SELECT id, unit_name, tech_level, name, code, faction_name FROM
Units JOIN Unit_Roles ON Units.id = Unit_Roles.uid
JOIN Roles ON Roles.role_id = Unit_Roles.rid
JOIN Factions ON fid = faction_id
{construct_filter_statement()}
GROUP BY id""")
    all_units = []
    for unit in extraction:  # put units in digestable form for website output
        if unit[2] == 4 or unit[2] == 0:  # unit is experimental or doesn't have a tech level
            result = f"{unit[3]} [{unit[4]}]"
        else:
            result = f"T{unit[2]} {unit[3]} [{unit[4]}]"  # example output: T1 Engineer [UAL0105]
        if unit[1]:  # unit has a name
            result = f"{unit[1]}: {result}"

        all_units.append((unit[0], result, unit[5].lower()))

    return render_template("home.html", units=all_units, button_toggles=convert_button_toggles_to_css_class())


@app.route('/', methods=['POST'])  # user pressed filter button on homepage
def home_filter_pressed():
    data = list(request.form)
    data = data[0]

    process_filter_button_pressed(data)

    return redirect("/")


@app.route('/faction/<string:faction>')
def faction(faction):
    filter = construct_filter_statement(faction)
    faction_extract = sql_statement(f"""
SELECT id, unit_name, tech_level, name, code, faction_name FROM
Units JOIN Unit_Roles ON Units.id = Unit_Roles.uid
JOIN Roles ON Roles.role_id = Unit_Roles.rid
JOIN Factions ON fid = faction_id
{filter}
GROUP BY id
ORDER BY faction_name, tech_level""")
    all_units = []
    for unit in faction_extract:  # put units in digestible form for website output
        if unit[2] == 4 or unit[2] == 0:  # unit is experimental or doesn't have a tech level
            result = f"{unit[3]} [{unit[4]}]"
        else:
            result = f"T{unit[2]} {unit[3]} [{unit[4]}]"  # example output: T1 Engineer [UAL0105]
        if unit[1]:  # unit has a name
            result = f"{unit[1]}: {result}"

        all_units.append((unit[0], result, unit[5].lower()))
    return render_template("faction.html", units=all_units, faction_site=faction, button_toggles=convert_button_toggles_to_css_class())


@app.route('/faction/<string:faction>', methods=['POST'])  # user pressed filter button on faction page
def filter_pressed(faction):
    data = list(request.form)
    data = data[0]

    process_filter_button_pressed(data)

    return redirect(f"/faction/{faction}")


@app.route('/unit/<int:id>')
def unit(id):
    unit_info = sql_statement(f"""
SELECT id, name, health, mass_cost, energy_cost, build_time, tech_level, faction_name FROM
Units JOIN Unit_Roles ON Units.id = Unit_Roles.uid
JOIN Roles ON Roles.role_id = Unit_Roles.rid
JOIN Factions ON fid = faction_id
WHERE id = {id}
GROUP BY id
ORDER BY faction_name, tech_level""")
    # unit_info[0] = id, [1] = name, [2-7] = health, mass cost, energy cost, build time, tech level, faction
    return render_template("unit.html", unit_id=id, unit=unit_info[0])


@app.route('/manage-units')
def manage_units():
    return render_template("manage_units.html", save_data={}, nt={})


@app.route('/manage-units', methods=['POST'])
def submitted_units():
    response = request.form

    nt = {}  # notifcation text

    save_data = dict(response)

    value_vs_display = {
    "add": "Add a unit",
    "update": "Update a unit",
    "delete": "Delete a unit",
    }
    save_data["submit desire display"] = value_vs_display[response["submit desire"]]
    save_data["submit desire value"] = response["submit desire"]
    empty_save_data = {}
    empty_save_data["submit desire display"] = value_vs_display[response["submit desire"]]
    empty_save_data["submit desire value"] = response["submit desire"]

    desire = ""
    all_units = []
    form_action = response["form_action"]
    desire = response["submit desire"]

    if form_action == "submit form" and desire == "delete":  # user submitted a unit for deletion
        delete_unit_id = int(save_data['delete_unit_id'])
        nt["successful termination"] = f"{construct_unit_title(delete_unit_id)} has been successfully terminated. 🤗"
        delete_unit_from_supreme_database(delete_unit_id)
    
    if desire == "delete" or desire == "update":  # user selected they would like to delete or update a unit
        extraction = sql_statement("""
SELECT id, unit_name, tech_level, name, code FROM
Units JOIN Unit_Roles ON Units.id = Unit_Roles.uid
JOIN Roles ON Roles.role_id = Unit_Roles.rid
JOIN Factions ON fid = faction_id
GROUP BY id""")
        for unit in extraction:  # put units in digestable form for website output
            if unit[2] == 4 or unit[2] == 0:  # unit is experimental or doesn't have a tech level
                result = f"{unit[3]}"
            else:
                result = f"T{unit[2]} {unit[3]}"  # example output: T1 Engineer [UAL0105]
            if unit[1]:  # unit has a name
                result = f"{unit[1]}: {result}"
            result = f"{unit[0]}. {result}"

            if form_action == "selecting unit to update" and int(save_data["update_unit_id"]) == unit[0]:
                save_data["update unit id"] = unit[0]
                save_data["update unit"] = result
                continue
            if form_action == "selecting unit to delete" and int(save_data["delete_unit_id"]) == unit[0]:
                save_data["delete unit id"] = unit[0]
                save_data["delete unit"] = result
                continue
            all_units.append((unit[0], result))
    
    if form_action == "submitting desire":  # user submitted what they wanted to do rather than submitting a form
        return render_template("manage_units.html", desire=desire, units=all_units, save_data=save_data, nt=nt)

    if form_action == "selecting unit to update":  # user selected a unit to update, commence fill in code
        unit_id = int(save_data["update_unit_id"])
        unit_info = sql_statement(f"""
SELECT id, name, health, mass_cost, energy_cost, build_time, tech_level, faction_name, fid, code, unit_name, role_name FROM
Units JOIN Unit_Roles ON Units.id = Unit_Roles.uid
JOIN Roles ON Roles.role_id = Unit_Roles.rid
JOIN Factions ON fid = faction_id
WHERE id = {unit_id}
GROUP BY id
ORDER BY faction_name, tech_level""")
        unit_info = unit_info[0]
        save_data["unit_name"] = unit_info[1]
        save_data["unit_health"] = unit_info[2]
        save_data["unit_mass_cost"] = unit_info[3]
        save_data["unit_energy_cost"] = unit_info[4]
        save_data["unit_build_time"] = unit_info[5]
        save_data["unit_tech_level"] = unit_info[6]
        save_data["unit_faction_name"] = unit_info[7]
        save_data["unit_faction_id"] = unit_info[8]
        save_data["unit_code"] = unit_info[9]
        save_data["unit_unit_name"] = unit_info[10]
    
        for role_entry in unit_info:
            print(role_entry[11])
            #save_data[role_entry[11]] = role_entry
    
    if form_action == "submit form" and desire == "add":  # user submitted a unit to add
        nt = validate_unit(save_data)

        has_error = False
        for error in nt.values():  # checks for complaints
            if error != None:  # complaint detected
                has_error = True
                break
        if not has_error:  # no errors found with unit
            save_data = empty_save_data
            # add unit to supreme database


    # bullet proofing:

    # unit_name = response["unit_name"]
    # if len(unit_name) < 2 or len(unit_name) > 25:
    #     nt["unit_name"] = "Keep length between 2-25 characters."

    return render_template("manage_units.html", desire=desire, units=all_units, save_data=save_data, nt=nt)


@app.errorhandler(404)  # 404 page
def page_not_found(error):
    return render_template("404.html", title="cease this")


if __name__ == "__main__":
    app.run(debug=True)
