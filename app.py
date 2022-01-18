import sqlite3
from flask import Flask
import json

###########normalization of colors############
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 CREATE TABLE colors (
#                 id integer PRIMARY KEY AUTOINCREMENT,
#                 color varchar(30))
#                 """)
# cur.execute(sqlite_query)
# con.close()

# creating new table "animal_color" to identity all exists colors of animals
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 CREATE TABLE animal_color (
#                 animals_id varchar(10),
#                 color_id integer,
#                 FOREIGN KEY (color_id) REFERENCES colors (id))
#                 """)
# cur.execute(sqlite_query)
# con.close()

# creating new table temporary table
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 CREATE TABLE temp_table (
#                 temp integer)
#                 """)
# cur.execute(sqlite_query)
# con.close()


# adding color1 and color2 into temporary table
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 INSERT INTO temp_table
#                 SELECT distinct color1 FROM animals
#                 """)
# cur.execute(sqlite_query)
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 INSERT INTO temp_table
#                 SELECT distinct color2 FROM animals
#                 """)
# cur.execute(sqlite_query)
# con.commit()
# con.close()

#adding unique colors from temp table
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 INSERT INTO colors (color)
#                 SELECT DISTINCT RTRIM(temp) FROM temp_table
#                 WHERE temp NOT NULL
#                 """)
# cur.execute(sqlite_query)
# con.commit()
# con.close()

#adding indexes of colors and animals.color1/2 to the unifying table
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 INSERT INTO animal_color
#                 SELECT animals.animal_id, colors.id
#                 FROM animals
#                 JOIN colors ON rtrim(animals.color1)=rtrim(colors.color)
#                 GROUP BY animals.animal_id, colors.id
#                 """)
# cur.execute(sqlite_query)
# sqlite_query = ("""
#                 INSERT INTO animal_color
#                 SELECT animals.animal_id, colors.id
#                 FROM animals
#                 JOIN colors ON rtrim(animals.color2)=rtrim(colors.color)
#                 GROUP BY animals.animal_id, colors.id
#                 """)
# cur.execute(sqlite_query)
# con.commit()
# con.close()
#################################################

############normalization of animals types#######
#creating new table type of animal
#adding all animals types to the animal_type table
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 CREATE TABLE animal_type (
#                 id varchar(10),
#                 type varchar(20))
#                 """)
# cur.execute(sqlite_query)
# sqlite_query = ("""
#                 INSERT INTO animal_type
#                 SELECT DISTINCT animal_id, animal_type
#                 FROM animals
#                 """)
# cur.execute(sqlite_query)
# con.commit()
# con.close()
#################################################

############normalization of breeds#######
#creating new table breed of animal
#adding all animals types to the animal_type table
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 CREATE TABLE animal_breed (
#                 id varchar(10),
#                 breed varchar(20))
#                 """)
# cur.execute(sqlite_query)
# sqlite_query = ("""
#                 INSERT INTO animal_breed
#                 SELECT DISTINCT animal_id, breed
#                 FROM animals
#                 """)
# cur.execute(sqlite_query)
# con.commit()
# con.close()
######################################################


####normalization of the values of the outcomes#######
#creating new table with the values of the outcomes
#adding all values of outcomes to the outcomes table
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 CREATE TABLE outcomes (
#                 ind integer PRIMARY KEY AUTOINCREMENT,
#                 animals_id varchar(10),
#                 age_upon_outcome varchar(20),
#                 outcome_subtype varchar(20),
#                 outcome_type varchar(50),
#                 outcome_month integer,
#                 outcome_year integer)
#                 """)
# cur.execute(sqlite_query)
# sqlite_query = ("""
#                 INSERT INTO outcomes (ind, animals_id, age_upon_outcome, outcome_subtype, outcome_type, outcome_month, outcome_year)
#                 SELECT "index", animal_id, age_upon_outcome, outcome_subtype, outcome_type, outcome_month, outcome_year
#                 FROM animals
#                 """)
# cur.execute(sqlite_query)
# con.commit()
# con.close()
#################################################


####normalization of animals base################
#creating new table with information about animals
#adding all animals data
# con = sqlite3.connect("animal.db")
# cur = con.cursor()
# sqlite_query = ("""
#                 CREATE TABLE animal_base (
#                 animal_id varchar(10),
#                 name varchar(20),
#                 date_of_birth date)
#                 """)
# cur.execute(sqlite_query)
# sqlite_query = ("""
#                 INSERT INTO animal_base (animal_id, name, date_of_birth)
#                 SELECT animal_id, name, date_of_birth
#                 FROM animals
#                 """)
# cur.execute(sqlite_query)
# con.commit()
# con.close()
##################################################

app = Flask("HW_15")

@app.route('/animals/<itemid>')
def animal(itemid):
    con = sqlite3.connect("animal.db")
    cur = con.cursor()
    sqlite_query = (
                    "SELECT ind, animal_id, name, date_of_birth, type, breed, age_upon_outcome, outcome_subtype, outcome_type, outcome_month, outcome_year, color "
                    "FROM animal_base "
                    "LEFT JOIN animal_type ON animal_type.id=animal_base.animal_id "
                    "LEFT JOIN animal_breed ON animal_breed.id=animal_base.animal_id "
                    "LEFT JOIN outcomes ON outcomes.animals_id=animal_base.animal_id "
                    "LEFT JOIN animal_color ON animal_color.animals_id=animal_base.animal_id "
                    "LEFT JOIN colors ON animal_color.color_id=colors.id "
                    f"WHERE ind='{itemid}' "
                    )
    cur.execute(sqlite_query)
    executed_query = cur.fetchall()
    print(executed_query)
    data = []
    for i in executed_query:
        animal_inf = {
            "age_upon_outcome": i[6],
            "name": i[2],
            "type": i[4],
            "breed": i[5],
            "color": i[11],
            "birth_day": i[3],
            "outcome_subtype": i[7],
            "outcome_type": i[8],
            "outcome_month": i[9],
            "outcome_year": i[10]
            }
        data.append(animal_inf)
    if len(data)>1:
        data[0]['color'] = f"{data[0]['color']} - {data[1]['color']}"
        data.pop(1)
    print(data)
    return json.dumps(data)

if __name__ == "__main__":
    app.run(debug=True)


