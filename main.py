import sqlite3


DATABASE_FILE = "supreme_db.db"
with sqlite3.connect(DATABASE_FILE) as connection:
    cursor = connection.cursor()
    sql = "SELECT Units.name, Roles.name FROM Unit_Roles JOIN Units ON Unit_Roles.uid = Units.id JOIN Roles ON Unit_Roles.rid = Roles.id"
    cursor.execute(sql) #executes the SELECT statement on the chosen table
    results = cursor.fetchall() #stores the results in the results variable
    print(results)