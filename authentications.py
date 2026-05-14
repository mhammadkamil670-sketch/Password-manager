from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash,check_password_hash
from databases import get_con
from flask import session
from tools import encryption_master
def check(user):
    if user in [""," ","."]:
        return False
    if not 8<= len(user) <=30:
        return False
    return True
def register(username,password):
    if check(username) and check(password):
        password=generate_password_hash(password)
        con=get_con()       
        f=con.cursor()
        try:
            f.execute("SELECT username FROM users WHERE username=%s",(username,))
            usernames=f.fetchone()
            if  usernames:
                return {"message":"ACCOUNT ALREADY EXISTS"}            
            else:
                user_key=Fernet.generate_key().decode()
                user_key_enc=encryption_master(user_key)
                f.execute("INSERT INTO users (username,password,user_key) VALUES (%s,%s,%s)",(username,password,user_key_enc))
                con.commit()
                session["user"]=username
                return {"message":"ACCOUNT CREATED SUCCESSFULLY",
                "success":True}
        finally:
            con.close()
            f.close()                
    else:
        return {"message":"USERNAME OR PASSWORD ARE INVALID"}
def login(username,password):
    if check(username) and check(password):
        con=get_con()
        f=con.cursor()
        try:
            f.execute("SELECT username FROM users  WHERE username=%s",(username,))
            usernames1=f.fetchone()
            if usernames1:
                usernames1=usernames1[0]
                f.execute("SELECT password FROM users WHERE username=%s",(usernames1,))   
                password_2=f.fetchone()[0]  
                if check_password_hash(password_2,password):
                    session["user"]=username
                    return {"message":"LOGIN SUCCESSFUL",
                    "loggedin":True}
                else:                                                                       return {"message":"USERNAME OR PASSWORD ARE INCORRECT"}
            else:
                return {"message":"ACCOUNT DOESNT EXIST"}
        finally:
            con.close()
            f.close()                