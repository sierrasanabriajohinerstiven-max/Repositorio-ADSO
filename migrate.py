import sqlite3
import os

db_path = os.path.join('instance', 'app.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

try:
    c.execute("ALTER TABLE 'order' ADD COLUMN customer_name VARCHAR(100);")
    print("Added customer_name")
except Exception as e:
    print(e)

try:
    c.execute("ALTER TABLE 'order' ADD COLUMN customer_email VARCHAR(120);")
    print("Added customer_email")
except Exception as e:
    print(e)

conn.commit()
conn.close()
print("Migration completed")
