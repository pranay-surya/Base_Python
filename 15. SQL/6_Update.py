#Create connection between python and sql
import mysql.connector as myconn
mydb = myconn.connect(host = 'localhost',user = 'root',password = 'Pranay@sql',database = 'college')
dbcursor = mydb.cursor()

Update_val = "update college.student set name = %s where Id = %s "
Values =  ("Bob",5)
dbcursor.execute(Update_val,Values,)
mydb.commit()

print(dbcursor.rowcount,'Data Updated..!')