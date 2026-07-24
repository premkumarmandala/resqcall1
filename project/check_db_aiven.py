import pymysql

db_config = {
    'host': 'mysql-5e2f1d3-premkumarmandala123-60de.b.aivencloud.com',
    'port': 14962,
    'user': 'avnadmin',
    'password': 'AVNS_atDQUv-7b_APooFrmLV',
    'database': 'defaultdb',
    'cursorclass': pymysql.cursors.DictCursor
}

conn = pymysql.connect(**db_config)
with conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) as c FROM hospitals WHERE status='Active'")
    count = cur.fetchone()['c']
    print('defaultdb Active:', count)
    
db_config['database'] = 'resq_db'
try:
    conn = pymysql.connect(**db_config)
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) as c FROM hospitals WHERE status='Active'")
        count = cur.fetchone()['c']
        print('resq_db Active:', count)
except Exception as e:
    print('resq_db err:', e)
