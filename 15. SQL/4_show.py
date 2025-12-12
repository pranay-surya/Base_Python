#Create connection between python and sql
import mysql.connector as myconn
mydb = myconn.connect(host = 'localhost',user = 'root',password = '',database = 'School')
dbcursor = mydb.cursor()


# My_cursor.execute(‘select * from emp1’)
# Myresult = my_cursor.fechall()
# Use for printing table in python , but this method show only one record.....

dbcursor.execute('select * from college.student')
for db_data in dbcursor.fetchall():
    print(db_data)