import mysql.connector


"""
step to get access to DB :

1.install python mysql lib :use commande python for sql
2.instal mysql system workbench to get Connector/python :get acces to API
3.creat new DB  
---------------------------------------
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE wildcat_db")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)
-----------------------------------------  
4.Connect to new DB :
----------------------------------------- 
mydb = mysql.connector.connect(
     host="127.0.0.1",
     user="root",
     passwd="mab@50192379",
     database="wildcat_db"
      )
----------------------------------------- 
5.creat new table :
        -->Wildcat_DB
        -->column :CubeProgrammer_Release VARCHAR(255), 
                   Data_ID VARCHAR(255),
                   Size VARCHAR(255), 
                   Time VARCHAR(255), 
                   Debit VARCHAR(255)
        -->
        
----------------------------------------- 
mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE Wildcat_DB (CubeProgrammer_Release VARCHAR(255), Data_ID VARCHAR(255),Size VARCHAR(255), Time VARCHAR(255), Debit VARCHAR(255))")

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)
  
-------------------------------------------
6.add element to the new table :

-------------------------------------------
      sql = "INSERT INTO Wildcat_DB (CubeProgrammer_Release,Data_ID,Size,Time,Debit) VALUES (%s, %s, %s, %s, %s)"
        val = (cubrprogrammer_release, ID[item],size[item],time[item],Debit[item])
        mycursor.execute(sql, val)
        mydb.commit()
    
    print(mycursor.rowcount, "record inserted.")
    
    mycursor.execute("select * from Wildcat_DB ")
    
    myresult = mycursor.fetchall()
    
    for x in myresult:
      print(x)
-------------------------------------------

very important !!!
every time you can lose data from DB 
so try to add data into local fb like this :
-------------------------------------------
mycursor = mydb.cursor()

sql = "INSERT INTO Wildcat_DB (CubeProgrammer_Release,Data_ID,Size_ID,Time_ID,Debit) VALUES (%s, %s, %s, %s, %s)"
val = [
  ('v2.4.0', '0x01', '1.96288', '0.458', '4.2858'),
('v2.4.0', '0x03', '5.989344', '0.727', '8.2384'),
('v2.4.0', '0x04', '0.963912', '0.028', '34.4254'),
('v2.4.0', '0x05', '0.963912', '0.031', '31.0939'),
('v2.4.0', '0x06', '6.016576', '0.154', '39.0687'),
('v2.4.0', '0x21', '512', '24.501', '20.8971'),
('v2.4.0', '0x22', '128', '6.051', '21.1535'),
('v2.4.0', '0x23', '5769.5920', '258.513', '22.3184'),
('v2.4.0', '0x24', '766.688', '34.847', '22.0015'),

('v2.3.0', '0x01', '1.96288', '0.548', '3.5819'),
('v2.3.0', '0x03', '5.989344', '0.715', '8.3767'),
('v2.3.0', '0x04', '0.963912', '0.036000000000000004', '26.7753'),
('v2.3.0', '0x05', '0.963912', '0.033', '29.2095'),
('v2.3.0', '0x06', '6.016576', '0.164', '36.6864'),
('v2.3.0', '0x21', '512', '23.165', '22.1023'),
('v2.3.0', '0x22', '128', '5.9510000000000005', '21.509'),
('v2.3.0', '0x23', '5769.592000000001', '293.075', '19.6864'),
('v2.3.0', '0x24', '766.688', '32.941', '23.2746'),

('v2.2.1', '0x01', '1.96288', '0.682', '2.8781'),
('v2.2.1', '0x03', '5.989344', '1.138', '5.263'),
('v2.2.1', '0x04', '0.963912', '0.136', '7.0876'),
('v2.2.1', '0x05', '0.963912', '0.261', '3.6931'),
('v2.2.1', '0x06', '6.016576', '2.133', '2.8207'),
('v2.2.1', '0x21', '512', '85.135', '6.014'),
('v2.2.1', '0x22', '128', '20.911', '6.1212'),
('v2.2.1', '0x23', '5769.592000000001', '924.631', '6.2399'),
('v2.2.1', '0x24', '766.688', '121.599', '6.3051'),

('v2.2.0', '0x01', '1.96288', '0.678', '2.8951'),
('v2.2.0', '0x03', '5.989344', '1.145', '5.2309'),
('v2.2.0', '0x04', '0.963912', '0.138', '6.9849'),
('v2.2.0', '0x05', '0.963912', '0.14', '6.8851'),
('v2.2.0', '0x06', '6.016576', '0.898', '6.7'),
('v2.2.0', '0x21', '512', '82.941', '6.1731'),
('v2.2.0', '0x22', '128', '20.089', '6.3716'),
('v2.2.0', '0x23', '5769.592000000001', '931.147', '6.1962'),
('v2.2.0', '0x24', '766.688', '123.227', '6.2218')

]

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")

-------------------------------------------
6.get access/see data from column :

-------------------------------------------
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM customers")

myresult = mycursor.fetchall()

mycursor.execute("SELECT name, address FROM customers")

myresult2 = mycursor.fetchall()
for x in myresult:
  print(x)

print("\n")

for x in myresult2:
  print(x)

-------------------------------------------
7.sort/serach data :[where] [order by ]
-------------------------------------------


mycursor = mydb.cursor()

sql = "SELECT * FROM customers WHERE address = %s"
adr = ("Yellow Garden 2", )

mycursor.execute(sql, adr)

myresult = mycursor.fetchall()

for x in myresult:
  print(x)


#Python MySQL Order By

mycursor = mydb.cursor()

sql = "SELECT * FROM customers ORDER BY name"

mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
  

-------------------------------------------

8.delete table :
-------------------------------------------
mycursor = mydb.cursor()

mycursor.execute("DROP TABLE customers;")


mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)
-------------------------------------------
9.delete DB 




mycursor = mydb.cursor()

mycursor.execute("TRUNCATE TABLE customers;")


mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)



"""
mydb = mysql.connector.connect(
     host="127.0.0.1",
     user="root",
     passwd="mab@50192379",
     database="wildcat_db"
      )

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")

mycursor.execute("CREATE TABLE Wildcat_DB (CubeProgrammer_Release VARCHAR(255), Data_ID VARCHAR(255),Size VARCHAR(255), Time VARCHAR(255), Debit VARCHAR(255))")

sql = "INSERT INTO Wildcat_DB (CubeProgrammer_Release,Data_ID,Size,Time,Debit) VALUES (%s, %s, %s, %s, %s)"
val = [
  ('v2.4.0', '0x01', '1.96288', '0.458', '4.2858'),
('v2.4.0', '0x03', '5.989344', '0.727', '8.2384'),
('v2.4.0', '0x04', '0.963912', '0.028', '34.4254'),
('v2.4.0', '0x05', '0.963912', '0.031', '31.0939'),
('v2.4.0', '0x06', '6.016576', '0.154', '39.0687'),
('v2.4.0', '0x21', '512', '24.501', '20.8971'),
('v2.4.0', '0x22', '128', '6.051', '21.1535'),
('v2.4.0', '0x23', '5769.5920', '258.513', '22.3184'),
('v2.4.0', '0x24', '766.688', '34.847', '22.0015'),

('v2.3.0', '0x01', '1.96288', '0.548', '3.5819'),
('v2.3.0', '0x03', '5.989344', '0.715', '8.3767'),
('v2.3.0', '0x04', '0.963912', '0.036000000000000004', '26.7753'),
('v2.3.0', '0x05', '0.963912', '0.033', '29.2095'),
('v2.3.0', '0x06', '6.016576', '0.164', '36.6864'),
('v2.3.0', '0x21', '512', '23.165', '22.1023'),
('v2.3.0', '0x22', '128', '5.9510000000000005', '21.509'),
('v2.3.0', '0x23', '5769.592000000001', '293.075', '19.6864'),
('v2.3.0', '0x24', '766.688', '32.941', '23.2746'),

('v2.2.1', '0x01', '1.96288', '0.682', '2.8781'),
('v2.2.1', '0x03', '5.989344', '1.138', '5.263'),
('v2.2.1', '0x04', '0.963912', '0.136', '7.0876'),
('v2.2.1', '0x05', '0.963912', '0.261', '3.6931'),
('v2.2.1', '0x06', '6.016576', '2.133', '2.8207'),
('v2.2.1', '0x21', '512', '85.135', '6.014'),
('v2.2.1', '0x22', '128', '20.911', '6.1212'),
('v2.2.1', '0x23', '5769.592000000001', '924.631', '6.2399'),
('v2.2.1', '0x24', '766.688', '121.599', '6.3051'),

('v2.2.0', '0x01', '1.96288', '0.678', '2.8951'),
('v2.2.0', '0x03', '5.989344', '1.145', '5.2309'),
('v2.2.0', '0x04', '0.963912', '0.138', '6.9849'),
('v2.2.0', '0x05', '0.963912', '0.14', '6.8851'),
('v2.2.0', '0x06', '6.016576', '0.898', '6.7'),
('v2.2.0', '0x21', '512', '82.941', '6.1731'),
('v2.2.0', '0x22', '128', '20.089', '6.3716'),
('v2.2.0', '0x23', '5769.592000000001', '931.147', '6.1962'),
('v2.2.0', '0x24', '766.688', '123.227', '6.2218')

]

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")

mycursor.execute("select * from Wildcat_DB ")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
