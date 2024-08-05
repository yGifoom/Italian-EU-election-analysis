import numpy as np
import pandas as pd
import pyodbc
import csv

# 1. Example establish database connection
connection = pyodbc.connect("/home/ygifoom/Documents/04 - Projects/dma crap/towny candidates/PreferenzeEuropee_2019.accdb")
# 2. Run SQL query
cursor = connection.cursor()

tables = [row.table_name for row in cursor.tables()]
print(tables)
t = input("which table amongst \n{tables}")
while t not in tables:
    t = input(f"incorrect table, choose again \n{tables}")
    
cursor.execute(f'select * from {t};')

# 3. Store the contents in "cursor" in the CSV using file I/O
with open(f'Preferenze_europee_{t}.csv','w') as f:
    writer = csv.writer(f)
    writer.writerows([x[0] for x in cursor.description])
    writer.writerows(cursor)
    
# 4. Close the database connection
cursor.close()
connection.close()