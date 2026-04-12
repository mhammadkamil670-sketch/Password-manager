import sqlite3
def something():
    from tools import decryption_master,decryption_student
def tablecreation():
    with sqlite3.connect("passwords.db") as con:
        f=con.cursor()
        f.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,username TEXT UNIQUE,
    password TEXT,user_key TEXT)""")
        f.execute("""CREATE TABLE IF NOT EXISTS passwords(id INTEGER PRIMARY KEY,username TEXT,passwords TEXT,titles TEXT,password_id INTEGER)""")    
def getuserpasses(username):
    from tools import decryption_student
    with sqlite3.connect("passwords.db") as con:
        f=con.cursor()
        f.execute("SELECT titles,passwords,password_id FROM passwords WHERE username=?",(username,))
        rows=f.fetchall()   
        new_row=[]
        for title,password,pid in rows:
            password_mod=decryption_student(password,username)
            new_row.append((title,password_mod,pid))
        return new_row
def deletepass(username,password_id):
    with sqlite3.connect("passwords.db") as con:
        f=con.cursor()
        f.execute("DELETE FROM passwords WHERE username=? AND password_id=?",(username,password_id))
def get_secretkey(username):
    with sqlite3.connect("passwords.db") as con:
        f=con.cursor()
        f.execute("SELECT user_key FROM users WHERE username=?",(username,))   
        return f.fetchone()[0]       
def get_max_index(username):
    with sqlite3.connect("passwords.db") as con:
        f=con.cursor()
        f.execute("SELECT MAX(password_id) FROM passwords WHERE username =?",(username,))
        index=f.fetchone()[0]
        if not index:
            return 0
        else:
            return index
with sqlite3.connect("passwords.db") as con:
    f=con.cursor()
    f.execute("SELECT * FROM passwords")
    print(f.fetchall())        