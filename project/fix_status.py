import pymysql

dbs = [
    {'host':'localhost', 'port':3306, 'user':'root', 'password':'Jesus143', 'db':'resq_db'},
    {'host':'mysql-5e2f1d3-premkumarmandala123-60de.b.aivencloud.com', 'port':14962, 'user':'avnadmin', 'password':'AVNS_atDQUv-7b_APooFrmLV', 'db':'defaultdb'},
]

for db in dbs:
    try:
        conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], password=db['password'], database=db['db'])
        with conn.cursor() as cursor:
            try:
                cursor.execute("ALTER TABLE hospitals ADD COLUMN status VARCHAR(50) DEFAULT 'Active'")
                print(f"Added status column to {db['host']}")
            except pymysql.err.OperationalError as e:
                print(f"Column may already exist on {db['host']}: {e}")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Connection failed for {db['host']}: {e}")
