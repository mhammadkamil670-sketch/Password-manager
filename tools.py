from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
from databases import get_secretkey
load_dotenv()
def get_cipher():
    key=os.getenv("SECRET_KEY")
    cipher=Fernet(key.encode())
    return cipher
def encryption_master(password):
    cipher=get_cipher()
    return cipher.encrypt(password.encode()).decode()
def decryption_master(password_encrypted):
    cipher=get_cipher()
    return cipher.decrypt(password_encrypted.encode()).decode()   
def encryption_student(password,username):
    key=get_secretkey(username)    
    key_=decryption_master(key)
    cipher_s=Fernet(key_.encode())
    return cipher_s.encrypt(password.encode()).decode()
def decryption_student(password,username):
    key=get_secretkey(username)  
    key_=decryption_master(key)
    cipher_s=Fernet(key_.encode())
    return cipher_s.decrypt(password.encode()).decode()
            