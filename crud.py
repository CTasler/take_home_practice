from model import User, Reservation, db, connect_to_db
from sqlalchemy import func


def create_user(username):
    user = User(username=username)
    
    db.session.add(user)
    db.session.commit()
    
    return user

def get_user_id(username): 
    user = User.query.filter(User.username == username).first()
    if not user: 
        return None
    return user.user_id

def create_res(user_id, res_date, res_time): 
    res = Reservation(user_id=user_id, res_date=res_date, res_time=res_time)
    

if __name__ == "__main__": 
    from server import app 
    
    connect_to_db(app)
    