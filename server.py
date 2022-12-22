from flask import (Flask, render_template, request, session, flash, redirect, current_app, jsonify)
import crud
import model 

app = Flask(__name__)
app.secret_key = "secret_key"


TIMES = ["0000 - 0030", "0030 - 0100", "0100 - 0130", "0130 - 0200", "0200 - 0230", "0230 - 0300", "0300 - 0330", "0330 - 0400", "0400 - 0430", "0430 - 0500", "0500 - 0530", "0530 - 0600", "0600 - 0630", "0630 - 0700", "0700 - 0730", "0730 - 0800", "0800 - 0830", "0830 - 0900", "0900 - 0930", "0930 - 1000", "1000 - 1030", "1030 - 1100", "1100 - 1130", "1130 - 1200", "1200 - 1230", "1230 - 1300", "1300 - 1330", "1330 - 1400", "1400 - 1430", "1430 - 1500", "1500 - 1530", "1530 - 1600", "1600 - 1630", "1630 - 1700", "1700 - 1730", "1730 - 1800", "1800 - 1830", "1830 - 1900", "1900 - 1930", "1930 - 2000", "2000 - 2030", "2030 - 2100", "2100 - 2130", "2130 - 2200", "2200 - 2230", "2230 - 2300", "2300 - 2330", "2330 - 0000"]

# TIMES = ["12:00 AM - 12:30 AM", "12:30 AM - 01:00 AM", "01:00 AM - 01:30 AM", "01:30 AM - 02:00 AM", "02:00 AM - 02:30 AM", "02:30 AM - 03:00 AM", "03:00 AM - 03:30 AM", "03:30 AM - 04:00 AM", "04:00 AM - 04:30 AM", "04:30 AM - 05:00 AM", "05:00 AM - 05:30 AM", "05:30 AM - 06:00 AM", "06:00 AM - 06:30 AM", "06:30 AM - 07:00 AM", "07:00 AM - 07:30 AM", "07:30 AM - 0800 AM","08:00 AM - 08:30 AM", "08:30 AM - 09:00 AM", "09:00 AM - 09:30 AM", "09:30 AM - 10:00 AM", "10:00 AM - 10:30 AM", "10:30 AM - 11:00 AM", "11:00 AM - 11:30 AM", "11:30 AM - 12:00 PM", "12:00 PM - 12:30 PM", "12:30 PM - 01:00 PM", "01:00 PM - 01:30 PM", "01:30 PM - 02:00 PM ", "02:00 PM - 02:30 PM", "02:30 PM - 03:00 PM", "03:00 PM - 03:30 PM", "03:30 PM - 04:00 PM", "04:00 PM - 04:30 PM", "04:30 PM - 05:00 PM", "05:00 PM - 05:30 PM", "05:30 PM - 06:00 PM", "06:00 PM - 06:30 PM", "06:30 PM - 07:00 PM", "07:00 PM - 07:30 PM", "07:30 PM - 08:00 PM", "08:00 PM - 08:30 PM", "08:30 PM - 09:00 PM", "09:00 PM - 09:30 PM", "09:30 PM - 10:00 PM", "10:00 PM - 10:30 PM", "10:30 PM - 11:00 PM", "11:00 PM - 11:30 PM", "11:30 PM - 12:00 AM"]

@app.route("/")
def show_homepage():
    return render_template("homepage.html")

@app.route("/get-username")
def get_username():
    username = session["username"]
    print(username)
    return jsonify({"username": username})

@app.route('/results', methods=['POST'])
def show_results():
    date = request.json.get('date')
    start_time = request.json.get('start-time')
    end_time = request.json.get('end-time')
    print(f"{date}{start_time}{end_time}")
    
    new_start = ''
    for char in start_time: 
        if char != ":": 
            new_start += char
            
    new_end = ""
    for char in end_time: 
        if char != ":":
            new_end += char
            
    results = [time for time in TIMES if int(new_end) >= int(time[:4]) >= 
               int(new_start) and int(new_start) <= int(time[-4:]) 
               <= int(new_end)]
    
    return jsonify({"data": results})

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

@app.route("/check-reservations")
def check_reservations():
    date = request.args.get('date')
    print(date)
    user_id = crud.get_user_id(session["username"])
    reservations = crud.get_all_res_by_date(date=date, user_id=user_id)
    print(reservations)
    if reservations: 
        status = "not_available"
    else: 
        status = "available"
    return {"data": status}

@app.route("/create-reservation", methods=['POST'])
def create_reservation():
    date = request.json.get('date')
    time = request.json.get('time')
    
    user_id = crud.get_user_id(session["username"])
    print(f"{date}{time}{user_id}")
    print(type(date))
    print(type(time))
    crud.create_res(user_id=user_id, res_date=date, res_time=time)
    return jsonify({'result': "successful"})


if __name__ == "__main__":
    from model import connect_to_db
    
    connect_to_db(app)
    
    app.run(debug=True)