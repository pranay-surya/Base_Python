# Create connection between python and sql
import mysql.connector as myconn
mydb = myconn.connect(host = 'localhost',user = 'root',password = '',database = 'School')
dbcursor = mydb.cursor()

print("Connected..")