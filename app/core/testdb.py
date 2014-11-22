import sqlite3

_DB_PATH = os.path.join(_CUR_PATH, "data", "..", "sdms.db")
connection = sqlite3.connect(_DB_PATH, check_same_thread=False)

query = "insert into product values('NO00001', 'product_1', NULL)";
try:
    cur = connection.cursor()
    cur.execute(query)
    cur.close()
except:
    print "error"
finally:
    connection.close()
