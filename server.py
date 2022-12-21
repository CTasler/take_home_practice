from flask import (Flask, render_template, request, session, flash, redirect, current_app, jsonify)
import crud
import model 

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route("/")
def show_homepage():
    print(session["username"])
    return render_template("homepage.html")

@app.route('/login-page')
def show_login_page(): 
    return render_template("login-page.html")
    

@app.route("/process-login", methods=['POST'])
def login_user():
    username = request.json.get("username")
    session["username"] = username
    print(session["username"])
    
    user_id = crud.get_user_id(username)
    if not user_id: 
        crud.create_user(username)
        
    return redirect("/")



if __name__ == "__main__":
    from model import connect_to_db
    
    connect_to_db(app)
    
    app.run(debug=True)