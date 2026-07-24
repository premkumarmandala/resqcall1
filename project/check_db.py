import pymysql

conn=pymysql.connect(host='mysql-5e2f1d3-premkumarmandala123-60de.b.aivencloud.com', port=14962, user='avnadmin', password='AVNS_atDQUv-7b_APooFrmLV', database='defaultdb', cursorclass=pymysql.cursors.DictCursor)
c=conn.cursor()
c.execute("SELECT id, name, status FROM hospitals WHERE status='Active'")
res=c.fetchall()
print(f'Active hospitals: {len(res)}')
