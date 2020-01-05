#W3 schools
import mysql.connector

# CREATE DATABASE

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd=""
# )

# mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE mydatabase")

#   host="localhost",
#   user="root",
#   passwd=""
# )

# mycursor = mydb.cursor()

# mycursor.execute("SHOW DATABASES")

# for x in mycursor:
#   print(x)

# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="",
#   database="mydatabase"
# ) 

#CREATE TABLE In CREATED DATABASE

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="",
#   database="mydatabase"
# )

# mycursor = mydb.cursor()

# # mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
# # mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))") 
# mycursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY") 

# mycursor.execute("SHOW TABLES")

# for x in mycursor:
#   print(x) 

# INSERT INTO TABLE

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="mydatabase"
)
mycursor = mydb.cursor()

# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("John", "Highway 21")
# mycursor.execute(sql, val)

# mydb.commit()

# print(mycursor.rowcount, "record inserted.")

# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = [
#   ('Peter', 'Lowstreet 4'),
#   ('Amy', 'Apple st 652'),
#   ('Hannah', 'Mountain 21'),
#   ('Michael', 'Valley 345'),
#   ('Sandy', 'Ocean blvd 2'),
#   ('Betty', 'Green Grass 1'),
#   ('Richard', 'Sky st 331'),
#   ('Susan', 'One way 98'),
#   ('Vicky', 'Yellow Garden 2'),
#   ('Ben', 'Park Lane 38'),
#   ('William', 'Central st 954'),
#   ('Chuck', 'Main Road 989'),
#   ('Viola', 'Sideway 1633')
# ]

# mycursor.executemany(sql, val)

# mydb.commit()

# print(mycursor.rowcount, "was inserted.") 


# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("Michelle", "Blue Village")
# mycursor.execute(sql, val)

# mydb.commit()

# print("1 record inserted, ID:", mycursor.lastrowid) 

# SELECTING FROM DATABASE

# mycursor.execute("SELECT * FROM customers")

# myresult = mycursor.fetchall()

# for x in myresult:
#   print(x)

# myresult = mycursor.fetchone()

# print(myresult) 

# mycursor.execute("SELECT name FROM customers")

# myresult = mycursor.fetchall()

# for x in myresult:
#   print(x) 

# SELECT PARTICULAR

# sql = "SELECT * FROM customers WHERE address ='Sky st 331'"
# sql = "SELECT * FROM customers WHERE address LIKE '%way%'" # contains the word way
# mycursor.execute(sql)

# myresult = mycursor.fetchall()

# for x in myresult:
#   print(x)

sql = "SELECT * FROM customers WHERE address = %s"
adr = ("Yellow Garden 2", )

mycursor.execute(sql, adr)

myresult = mycursor.fetchall()

for x in myresult:
  print(x) 

