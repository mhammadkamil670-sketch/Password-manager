from dotenv import load_dotenv
import psycopg2
import os
load_dotenv()
def get_con():
    return psycopg2.connect(os.getenv("DATABASE_URL2.0"),
sslmode="require")
def something():
    from tools import decryption_master,decryption_student
def getuserpasses(username):
    from tools import decryption_student
    con=get_con()
    f=con.cursor()
    try:
        f.execute("SELECT titles,passwords,password_id FROM passwords WHERE username=%s",(username,))
        rows=f.fetchall()   
        new_row=[]
        for title,password,pid in rows:
            password_mod=decryption_student(password,username)
            new_row.append((title,password_mod,pid))
        return new_row
    finally:
        con.close()
        f.close()
def deletepass(username,password_id):
    con=get_con()
    f=con.cursor()
    try:
        f.execute("DELETE FROM passwords WHERE username=%s AND password_id=%s",(username,password_id))
    finally:
        con.commit()
        con.close()
        f.close()
def get_secretkey(username):
    con=get_con()
    f=con.cursor()
    try:
        f.execute("SELECT user_key FROM users WHERE username=%s",(username,))   
        return f.fetchone()[0]    
    finally:
        con.close()
        f.close()   
def get_max_index(username):
    con=get_con()
    f=con.cursor()
    try:
        f.execute("SELECT MAX(password_id) FROM passwords WHERE username =%s",(username,))
        index=f.fetchone()[0]
        if not index:
            return 0
        else:
            return index   
    finally:
        con.close()
        f.close()                     