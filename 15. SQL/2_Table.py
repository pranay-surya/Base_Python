#Create connection between python and sql
import mysql.connector as myconn
mydb = myconn.connect(host = 'localhost',user = 'root',password = '',database = 'School')
dbcursor = mydb.cursor()

# Create Table in database college
dbcursor.execute("""
CREATE TABLE student (
    ID INT,
    Name VARCHAR(50),
    Year INT,
    Fees_Paid VARCHAR(60)
)
""")

print("Table Created..")