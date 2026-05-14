import random
from databases import get_max_index,get_con
from tools import encryption_student,decryption_student
def password_gen(length=8):
    length=int(length)
    if 8>=length or length>=30:
        return "ERROR"
    else:
        alphabet_upper = [ 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']   
        numbers_ = ['0','1','2','3','4','5','6','7','8','9']
        symbols_ = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*','+', ',', '-', '.', '/', ':', ';', '<', '=', '>','?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
        random.shuffle(alphabet_upper)
        random.shuffle(alphabet)
        random.shuffle(numbers_)
        random.shuffle(symbols_)
        l=int(length/4)
        a_u=alphabet_upper[:l]
        a=alphabet[:l]
        n=numbers_[:l]
        s=symbols_[:l]
        password=a_u+a+n+s
        password="".join(password)
        return password
def savepassword(username,password,title):
    current_m_index = get_max_index(username)
    con = get_con()
    password_enc = encryption_student(password, username)
    f = con.cursor()
    try:
        new_max_index=current_m_index+1
        f.execute("INSERT INTO passwords(username,passwords,titles,password_id) VALUES (%s,%s,%s,%s)",(username,password_enc,title,new_max_index))
        con.commit()
        return new_max_index
    finally:
        con.close()
        f.close()    
def passwordcheck(password):
    score=0
    if len(password)<8:
        return "PASSWORD IS WEAK"
    if len(password)==8:
        score+=2
    elif len(password) <=12 and len(password)>8:
        score+=4
    elif len(password) >=16:
        score+=6
    sym=[]
    ns=[]
    as_l=[]
    as_u=[]    
    for i in password:
        if  i in   ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*','+', ',', '-', '.', '/', ':', ';', '<', '=', '>','?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']:
            sym.append(i)
        if i in  ['0','1','2','3','4','5','6','7','8','9']:
            ns.append(i)     
        if i in  ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
            as_l.append(i)
        if i in  [ 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
            as_u.append(i)    
    if  len(sym) >1:
        score+=1
    if len(ns)>1:
        score+=1
    if len(as_l)>1:
        score+=1
    if len(as_u)>1:
        score+=1
    if score <=4:
        return "PASSWORD IS WEAK"
    elif score<=8 and score>4:
        return "PASSWORD IS DESCENT"
    else:
        return "PASSWORD IS SECURE"
def queryfortitle(username,password_id):
    con=get_con()
    f=con.cursor()
    try:
        f.execute("SELECT titles FROM passwords WHERE username=%s AND password_id=%s",(username,password_id))
        titles=f.fetchall()[0]
        if not titles:
            return "ERROR"
        return titles
    finally:
        con.close()
        f.close()    