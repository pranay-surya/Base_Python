#Create connection between python and sql
import mysql.connector as myconn
mydb = myconn.connect(host = 'localhost',user = 'root',password = '',database = 'School')
dbcursor = mydb.cursor()

data = [
    (2, 'Bob', 2022, 'No'),
    (3, 'Charlie', 2023, 'Yes'),
    (4, 'Diana', 2024, 'No'),
    (5, 'Ethan', 2023, 'Yes')
]
data_1 = [
    (6, 'Fiona', 2022, 'Yes'),
    (7, 'George', 2023, 'No'),
    (8, 'Hina', 2024, 'Yes'),
    (9, 'Ivan', 2022, 'Yes'),
    (10, 'Jaya', 2023, 'No'),
    (11, 'Kunal', 2024, 'Yes'),
    (12, 'Lina', 2023, 'No'),
    (13, 'Mohit', 2022, 'Yes'),
    (14, 'Nina', 2024, 'Yes'),
    (15, 'Omkar', 2023, 'No')
]


dbcursor.executemany("INSERT INTO student (ID, Name, Year, Fees_Paid) VALUES (%s, %s, %s, %s)", data_1)
mydb.commit()