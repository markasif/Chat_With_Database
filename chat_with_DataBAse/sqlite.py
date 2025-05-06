import sqlite3

connection=sqlite3.connect("student.db")

cursor=connection.cursor()

table_info = """
create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT)

"""

cursor.execute(table_info)

cursor.execute('''Insert INTO STUDENT values ('Krish','Data Science','A',90)''')
cursor.execute('''Insert INTO STUDENT values ('Rahul','Big Data','B',80)''')
cursor.execute('''Insert INTO STUDENT values ('Ishwar','Data Mining','C',70)''')
cursor.execute('''Insert INTO STUDENT values ('Asif','AI/ML Manager','A',90)''')
cursor.execute('''Insert INTO STUDENT values ('Favas','Data','A',90)''')

print("the insert records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

connection.commit()
connection.close()