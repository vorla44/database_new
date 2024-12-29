import sqlite3

# establish a connection and a cursor
connection = sqlite3.connect("data2.db")
cursor = connection.cursor()

# Query all data
cursor.execute ("SELECT * FROM events WHERE band='Lions'")
rows = cursor.fetchall()
print(rows) # lista

# Query certain data
cursor.execute ("SELECT band, date FROM events WHERE band='Lions'")
rows = cursor.fetchall()
print(rows) # lista

# Insert new rows
new_rows = [('Lions', 'Lion City', '2088.10.15'),
            ('Lions', 'Lion City', '2088.10.15')
            ]
cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit()

