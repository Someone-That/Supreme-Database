from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

connection = sqlite3.connect('supreme_db.db')
tech_filter = []
faction_filter = []
role_filter = []

button_order = ['1', '2', '3', '4', "UEF", "Aeon", "Cybran", "Seraphim", "Land", "Air", "Naval", "Anti Air", "Anti Naval"]
button_toggles = [False, False, False, False, False, False, False, False, False, False, False, False, False]


def sql_statement(connection, sql):
    '''executes sql statement'''
    try:
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


@app.route('/')
def home():
    connection = sqlite3.connect('supreme_db.db')
    extraction = sql_statement(connection, f"""
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
    connection = sqlite3.connect('supreme_db.db')
    filter = construct_filter_statement(faction)
    faction_extract = sql_statement(connection, f"""
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
    connection = sqlite3.connect('supreme_db.db')
    unit_info = sql_statement(connection, f"""
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
    return render_template("manage_units.html")


@app.route('/manage-units', methods=['POST'])
def submitted_units():
    connection = sqlite3.connect('supreme_db.db')
    save_data = {
    "submit desire": "",
    "unit_name": "",
    "unit_health": "",
    "unit_mass_cost": "",
    "unit_energy_cist": "",
    "unit_build_time": "",
    "unit_tech_level": "",
    "unit_faction": "",
    "unit_code": "",
    "unit_unit_name": ""}

    response = request.form
    nt = {}  # nt = notification text

    desire = ""
    all_units = []
    if response["is_submitting_desire"]:  # user submitted what they wanted to do rather than submitting a form
        desire = response["submit desire"]
    
    if desire == "delete" or desire == "update":
        extraction = sql_statement(connection, """
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

            all_units.append((unit[0], result))

    # bullet proofing:

    # unit_name = response["unit_name"]
    # if len(unit_name) < 2 or len(unit_name) > 25:
    #     nt["unit_name"] = "Keep length between 2-25 characters."

    return render_template("manage_units.html", desire=desire, units=all_units)


@app.errorhandler(404)  # 404 page
def page_not_found(error):
    return render_template("404.html", title="cease this")


if __name__ == "__main__":
    app.run(debug=True)
