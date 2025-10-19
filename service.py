from session import Session
from utils import Response, match_password, hash_password
from db import cur, auto_commit
from models import User
session = Session()




def login(username : str, password : str):
    user = session.check_session()
    if user:
        return Response('you already logged in',404)
    
    get_user_by_username = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username,(username,))


    user_data = cur.fetchone()

    if not user_data:
        return Response('user not found',404)
    

    user = User.from_tuple(user_data)
    if not match_password(password, user.password):
        return Response('password wrong',404)
    
    session.add_session(user)
    return Response('you successfully logged in')


def log_out():
    if session.session:
        session.session = None
        return Response('You have successfully logged out', 200)
    
    return Response('No active session found', 404)


@auto_commit
def register(username, password, role):
    cur.execute("""
        INSERT INTO users (username, password, role)
        VALUES (%s, %s, %s)
    """, (username, hash_password(password), role))

    return Response("User registered successfully", 201)
