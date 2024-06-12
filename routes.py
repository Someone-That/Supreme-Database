from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)

connection = sqlite3.connect('supreme_db.db')


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


@app.route('/')
def home():
    connection = sqlite3.connect('supreme_db.db')
    extraction = sql_statement(connection, "SELECT id, unit_name, tech_level, name, code FROM Units")
    all_units = []
    for unit in extraction:  # put units in digestable form for website output
        if unit[2] == 4:  # unit is experimental
            result = f"{unit[3]} [{unit[4]}]"
        else:
            result = f"T{unit[2]} {unit[3]} [{unit[4]}]"  # example output: T1 Engineer [UAL0105]
        if unit[1]:  # unit has a name
            result = f"{unit[1]}: {result}"
        
        all_units.append((unit[0],result))
    return render_template("home.html", units=all_units)


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
