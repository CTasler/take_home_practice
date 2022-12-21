from flask_sqlalchemy import SQLAlchemy
import os 

db = SQLAlchemy()

# os.system("dropdb melonsite")
# os.system("createdb melonsite")

class User(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    
    reservation = db.relationship("Reservation", back_populates="user")
    
class Reservation(db.Model):
    __tablename__ = "reservations"
    
    res_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    res_date = db.Column(db.Date, nullable=False)
    res_time = db.Column(db.Time, nullable=False)
    
    user = db.relationship("User", back_populates="reservation")
    
    
def connect_to_db(app, db_uri="postgresql:///melonsite"):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print("Connected to the db!")
    
    
if __name__=="__main__": 
    from server import app 
    
    with app.app_context():
        connect_to_db(app)
        db.create_all()
        db.session.commit()