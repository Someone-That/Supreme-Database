from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

connection = sqlite3.connect('supreme_db.db')
tech_filter = []
faction_filter = []
role_filter = []


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


def construct_filter_statement(faction_site = ""):
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
        return
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
    return render_template("home.html", units=all_units)


@app.route('/', methods=['POST'])
def home_filter_pressed():
    data = list(request.form)
    data = data[0]

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
    
    print(tech_filter, role_filter, faction_filter)
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
    return render_template("faction.html", units=all_units, faction_site=faction)


@app.route('/faction/<string:faction>', methods=['POST'])
def filter_pressed(faction):
    data = list(request.form)
    data = data[0]

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
    
    print(tech_filter, role_filter, faction_filter)
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


@app.errorhandler(404)  # 404 page
def page_not_found(error):
    return render_template("404.html", title="cease this")


if __name__ == "__main__":
    app.run(debug=True)
