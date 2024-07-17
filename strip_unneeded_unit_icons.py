import os
import sqlite3

DATABASE_FILE = "supreme_db.db"


def sql_statement(sql):
    '''executes sql statement'''
    try:
        with sqlite3.connect(DATABASE_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
    except:
        return


icons_path = "static/icons/units/"

all_icons = os.listdir(icons_path)
code_extraction = sql_statement("SELECT code FROM Units;")

delete_list = []
outlier_list = []

#  rename all icons to just the code and capitalise
for icon in all_icons:
    os.rename(f"{icons_path}{icon}", f"{icons_path}{icon[:7].upper()}.png")

#  check for units not included
# for code in code_extraction:
#     should_delete = True
#     for icon in all_icons:
#         uc = code[0]
#         uc = uc.lower()
#         if uc in icon.lower():
#             should_delete = False
#             break
#     if should_delete:
#         outlier_list.append(code)
# print(outlier_list)

#  delete all irrelevant icons
# for icon in all_icons:
#     should_delete = True
#     for code in code_extraction:
#         if code[0].lower() in icon.lower():
#             should_delete = False
#             break
#     if should_delete:
#         delete_list.append(icon)
#         os.remove(f"{icons_path}{icon}")


