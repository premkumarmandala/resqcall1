import MySQLdb
db = MySQLdb.connect(host='localhost', user='root', passwd='Jesus143', db='resq_db')
cursor = db.cursor()
cursor.execute("DESC hospitals")
for row in cursor.fetchall():
    print(row[0])
db.close()
