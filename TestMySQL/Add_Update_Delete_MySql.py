import mysql.connector

server="localhost"
port=3306
database="studentmanagement"
username="root"
password="@Obama123"

conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)

#Them 1 student
cursor=conn.cursor()
sql="insert into student (code, name, age) values (%s, %s, %s)"
val=("sv09","Ha",28)
cursor.execute(sql,val)
conn.commit()

print(cursor.rowcount," record inserted")

cursor.close()

#Them nhieu student
cursor = conn.cursor()
sql="insert into student (code,name,age) values (%s,%s,%s)"
val=[
    ("sv10","Trần Quyết Chiến",19),
    ("sv11","Hồ Thắng",22),
    ("sv12","Hoàng Hà",25),
     ]
cursor.executemany(sql,val) #thuc thi nhieu
conn.commit()

print(cursor.rowcount," record inserted")

cursor.close()

#Update
cursor = conn.cursor()
sql="update student set name='Hoàng Lão Tà' where Code='sv09'"
cursor.execute(sql)

conn.commit()

print(cursor.rowcount," record(s) affected")
cursor.close()

#Update with SQL injection
cursor = conn.cursor()
sql="update student set name=%s where Code=%s"
val=('Hoàng Lão Tà','sv09')
cursor.execute(sql,val)

conn.commit()

print(cursor.rowcount," record(s) affected")
cursor.close()

#Delete
cursor = conn.cursor()
sql="DELETE from student where ID=10"
cursor.execute(sql)

conn.commit()

print(cursor.rowcount," record(s) affected")
cursor.close()

#Delete with SQL injection
cursor = conn.cursor()
sql = "DELETE from student where ID=%s"
val = (13,)

cursor.execute(sql, val)

conn.commit()

print(cursor.rowcount," record(s) affected")
cursor.close()