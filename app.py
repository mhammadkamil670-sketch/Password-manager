from flask import Flask,request,render_template,jsonify,session,redirect
import os
from authentications import register,login
from passwordhandler import password_gen,savepassword,passwordcheck,queryfortitle
from databases import tablecreation,getuserpasses,deletepass
from dotenv import load_dotenv
import os
tablecreation()
load_dotenv()
app=Flask(__name__)
key=os.getenv("SESSION_KEY")
app.secret_key=key
@app.route("/",methods=["GET"])
def about():
    if "user" in session:
        return redirect("/passwords")    
    return render_template("about.html")
@app.route("/next1",methods=["GET"])
def about1():
    if "user" in session:
        return redirect("/passwords")    
    return render_template("abouts.html")
@app.route("/next2",methods=["GET"])  
def rl():
    if "user" in session:
        return redirect("/passwords")    
    return render_template("choice.html")
@app.route("/register",methods=["GET"])
def indexr():
    if "user" in session:
        return redirect("/passwords")
    return render_template("register.html")
@app.route("/register",methods=["POST"])
def registers():
    if "user" in session:
        return redirect("/passwords")    
    data=request.get_json()
    username=data.get("username")  
    password=data.get("password")
    return jsonify(register(username,password))
@app.route("/login",methods=["GET"])
def indexl():  
    if "user" in session:
        return redirect("/passwords")
    return render_template("login.html")
@app.route("/login",methods=["POST"])
def logins():
    if "user" in session:
        return redirect("/passwords")    
    data=request.get_json()
    username=data.get("username")  
    password=data.get("password")
    return jsonify(login(username,password))
@app.route("/passwords",methods=["GET"])    
def index2():
    if not "user" in session:
        return redirect("/")
    username=session["user"]
    passwords=getuserpasses(username)
    return render_template("passwordhandling.html",passwords=passwords)
@app.route("/passwords",methods=["POST"])    
def passwordhandling():
    if not "user" in session:
        return jsonify({"login":False})      
    data=request.get_json()
    username=session["user"]
    message=data.get("message")
    if "generate" in message:
        infoforpass=message.split()
        passleng=infoforpass[1]
        passtitle=" ".join(infoforpass[2:])
        p=password_gen(passleng)
        if p=="EROR":
            return jsonify({"error":"Something went wrong"}),400
        id_new=savepassword(username,p,passtitle)
        return jsonify({"message":{"pass":p,
        "tit":passtitle,
        "idval":id_new}})
    if "delete" in message[:6]:
        passw=message.split()[1:]
        try:
            passw=passw[0]
        except:
            return jsonify({"error":"ERROR"}),400
        deletepass(username,passw) 
        return jsonify({"message":"Deleted successfully"})
@app.route("/logout",methods=["GET"])
def logout():
    if not "user" in session:
        return redirect("/") 
    session.pop("user",None)    
    return redirect("/")      
if __name__ == "__main__":
    tablecreation()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)              