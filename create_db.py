import mysql.connector as sql
def create_db():
    con=sql.connect(host="localhost", user="root", password="jayraj11",database="IMS")
    
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTO_INCREMENT, name TEXT, email TEXT, gender TEXT, contact TEXT, dob TEXT, doj TEXT, pass TEXT, utype TEXT, address TEXT,salary TEXT)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTO_INCREMENT, name TEXT, contact TEXT, descr TEXT)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTO_INCREMENT, name TEXT)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTO_INCREMENT, Category TEXT, Supplier  TEXT, name TEXT,price text, qty text, status text)")
    con.commit()

create_db()