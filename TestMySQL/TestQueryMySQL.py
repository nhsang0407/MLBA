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

#Truy van toan bo sinh vien
cursor=conn.cursor()
sql="select * from student"
cursor.execute(sql)

dataset=cursor.fetchall()
print(dataset)

align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID',"Code","Name","Age"))
for item in dataset:
    id = item[0]
    code = item[1]
    name = item[2]
    age = item[3]
    avatar = item[4]
    intro = item[5]
    print(align.format(id,code,name,age))
cursor.close()
print("-"*40)

#Truy van sinh vien Age >=22 va <=26
cursor=conn.cursor()
sql="select * from student where age>=22 and age<=26"
cursor.execute(sql)
dataset=cursor.fetchall()

align="{0:<3} {1:<6} {2:<15} {3:<10}"
print(align.format("ID","Code","Name","Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()
print("-"*40)

#Truy van toan bo sinh vien theo tuoi tang dan
cursor=conn.cursor()
sql="select * from student order by age asc"
        # sql = "SELECT * FROM student " \
        #      "ORDER BY Age ASC"
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()
print("-"*40)

#Truy van sinh vien tuoi tu 22-26 va xep giam dan
cursor=conn.cursor()
sql="Select * from student " \
    "where age>=22 and age<=26 " \
    "order by age desc"
cursor.execute(sql)
dataset=cursor.fetchall()

align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()
print("-"*40)

#Truy van sinh vien khi biet ID
cursor=conn.cursor()
sql="select * from student "\
    "where ID=1"
cursor.execute(sql)
dataset=cursor.fetchone() #tra ve 1 tuple, ko phai kieu list nhu fetchall
print(dataset)
if dataset!=None:
    id,code,name,age,avatar,intro=dataset
    print("Id=", id)
    print("code=", code)
    print("name=", name)
    print("age=", age)

cursor.close()
print("-"*40)

#Truy van dang phan trang student
cursor=conn.cursor()
sql="select * from student LIMIT 3 OFFSET 0" #lay 3 phan tu tu vi tri 0
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()
print()


cursor = conn.cursor()
sql="SELECT * FROM student LIMIT 4 OFFSET 3"
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()
print("-"*40)

#Truy van moi lan lay 3 sinh vien => so sinh vien muon lay =N=limit=step
print("PAGING!!!!!")
cursor = conn.cursor()
sql="SELECT count(*) FROM student" #Dem tong so dong
cursor.execute(sql)
dataset=cursor.fetchone()
print(dataset)
rowcount=dataset[0]

limit=3
step=3
for offset in range(0,rowcount,step):
    sql=f"SELECT * FROM student LIMIT {limit} OFFSET {offset}"
    cursor.execute(sql)

    dataset=cursor.fetchall()
    align='{0:<3} {1:<6} {2:<15} {3:<10}'
    print(align.format('ID', 'Code','Name',"Age"))
    for item in dataset:
        id=item[0]
        code=item[1]
        name=item[2]
        age=item[3]
        avatar=item[4]
        intro=item[5]
        print(align.format(id,code,name,age))

cursor.close()