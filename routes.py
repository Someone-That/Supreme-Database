from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)


def sql_statement(connection, sql):
    '''executes sql statement'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except:
        return


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/unit')
def unit():
    return render_template("unit.html")


@app.errorhandler(404)  # 404 page
def page_not_found(error):
    return render_template("404.html", title="cease this")


if __name__ == "__main__":
    app.run(debug=True)
