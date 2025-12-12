#Create connection between python and sql
import mysql.connector as myconn
mydb = myconn.connect(host = 'localhost',user = 'root',password = '',database = 'School')
dbcursor = mydb.cursor()


# For deleting the record in Table.....
data_delete = "delete from college.student where Name =%s"
db_value = ('Bob',)
dbcursor.execute(data_delete,db_value)
mydb.commit()

print(dbcursor.rowcount,'Record Deleted..!')


# For Deleting All the Records ....

""""
dbdeletedata = “truncate table CodeBlockAcademy.emp”
dbcursor.execute(db_deletedata)
mydb.commit() """