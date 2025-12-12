# Writing into a file
# write() function is used to write content to a file.
# w :: Open a file for writing
""" fileptr = open("essy.txt","w")
fileptr.write("Python Program")
fileptr.close() """



#Appending data into a file
# a :: Open a file for appending data at the end of file.
# It does not truncate the file.
""" fileptr = open("essy.txt","a")
fileptr.write("\nPython Program once again")
fileptr.write("\n................")
fileptr.close()  """


# Reading all the contents of the file
# read() function is used read content of a file.
# r :: Open a file for reading.
""" fileptr = open("essy.txt","r")
print(fileptr.read())
fileptr.close()h
 """


# Reading lines from the file
# readline() :: used to read a file line by line from the start
""" fileptr = open("essy.txt","r")
line_1 = fileptr.readline()
line_2 = fileptr.readline()
print(line_1)
print(line_2)
fileptr.close() """


# count number of character in file
""" count = 0
fileptr = open("essy.txt","r")
f_content = fileptr.read()
for i in f_content :
    if i.isalpha() :
        count = count + 1
print("Alphabets ::",count)  
fileptr.close()  """     


# count number of digit in file
""" count = 0
fileptr = open("essy.txt","r")
f_content = fileptr.read()
for i in f_content :
    if i.isdigit() :
        count = count + 1
print("Digit ::",count)  
fileptr.close()  """


# count alphanumric term in file
""" count = 0
special = 0
fileptr = open("essy.txt","r")
f_content = fileptr.read()
for i in f_content :
    if i.isalnum() :
        count = count + 1
    else:
        special = special + 1    
print("Alphanumric ::",count)  
print("Special Symbol",special)
fileptr.close()   """


""" fileptr = open("essy.txt","a")
fileptr.write("\nPython Program once again")
fileptr.write("\n................")
fileptr.write("\n12345432347389")
fileptr.write("\npppp@jj")
fileptr.close()  """