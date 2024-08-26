# database creation and table creation using python

# this is using mysql.connector
# if we use mysql, then first we need to manually create 
# database 'bikedata' in mysql then only we can proceed

# import mysql.connector as mc
# conn = mc.connect(host='localhost', user='root', password='root', database='bikedata')
# if (conn.is_connected()):
#     print('connection established')
# else:
#     print('connection not established')


# using sqlite3

import sqlite3
conn = sqlite3.connect('bikedata.db')  #database name

query_to_create_table = """
create table BikeDetails (
    brand varchar (25),
    kms_driven int,
    owner int,
    age int,
    power int,
    predicted_price float
)
"""
# no need to put semicolon in the last

cur = conn.cursor()
cur.execute(query_to_create_table)
print("your database and table is created")
cur.close()
conn.close()