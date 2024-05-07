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
    all_units = sql_statement(connection, "SELECT id, name FROM Units")
    return render_template("home.html", units=all_units)


@app.route('/<int:id>')
def unit(id):
    connection = sqlite3.connect('supreme_db.db')
    unit_info = sql_statement(connection, f"SELECT * FROM Units WHERE id = {id}")
    # unit_info[0] = id, [1] = name, [2-5] = health, mass cost, energy cost, build time
    return render_template("unit.html", unit_id=id, unit=unit_info[0])


@app.errorhandler(404)  # 404 page
def page_not_found(error):
    return render_template("404.html", title="cease this")


if __name__ == "__main__":
    app.run(debug=True)
