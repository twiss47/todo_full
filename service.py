from session import Session
from utils import Response, match_password, hash_password, login_required,is_admin
from db import cur, auto_commit
from models import User, TodoType
from service import auto_commit
from logger_config import logger
session = Session()




def login(username : str, password : str):
    logger.info(f'user {username} is trying to login')
    user = session.check_session()
    if user:
        logger.warning(f'user {username} is already in system')
        return Response('you already logged in',404)
    
    get_user_by_username = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username,(username,))


    user_data = cur.fetchone()

    if not user_data:
        logger.error(f'user {username} not found')
        return Response('user not found',404)
    

    user = User.from_tuple(user_data)
    if not match_password(password, user.password):
        logger.error('wrong password')
        return Response('password wrong',404)
    
    session.add_session(user)
    logger.info(f'user {username} is successfully logged in')
    return Response('you successfully logged in')


def log_out():
    if session.session:
        session.session = None
        logger.info('you have already logged out')
        return Response('You have successfully logged out', 200)
    
    logger.warning('you have already logged out')
    return Response('No active session found', 404)


@auto_commit
def register(username, password, role):
    logger.info('user is registiring')
    cur.execute("""
        INSERT INTO users (username, password, role)
        VALUES (%s, %s, %s)
    """, (username, hash_password(password), role))

    logger.info('user successfully registired')
    return Response("User registered successfully", 201)




@login_required
@is_admin
@auto_commit
def add_todo(title: str, description: str | None = None):
    user = session.session
    try:
        logger.info('admin is adding new todo')

        insert_todo_query = '''
        INSERT INTO todos (title, user_id, todo_type, description)
        VALUES (%s, %s, %s, %s)
        '''
        cur.execute(insert_todo_query, (title, user.id, TodoType.PERSONAL.value, description))

        logger.info('todo successfully added')
        return Response('✅ Todo successfully inserted', 201)
    except Exception as e:
        logger.exception('something went wrong in function')
        return Response("Internal server error", 500)



@login_required
@is_admin
@auto_commit
def update_admin_role(user_id):
    try:
        logger.info('admin is changing user role')

        all_users_query = '''select * from users where role = 'user';'''
        cur.execute(all_users_query)
        users = cur.fetchall()

        logger.debug(f'current users: {[u for u in users]}')

        update_admin_role_query = '''update users set role = 'admin' where id = %s;'''
        cur.execute(update_admin_role_query, (user_id,))

        logger.info('user role is successfully changed to admin')
        return Response('user successfully updated', 202)
    except Exception:
        logger.exception("something went wrong in fuction")
        return Response("Internal server error", 500)


@login_required
@is_admin
@auto_commit
def get_user_todo():
    user = session.session
    try:
        logger.info('admin is watching user s todos')

        query = """SELECT id, title, description, todo_type FROM todos WHERE user_id = %s;"""
        cur.execute(query, (user.id,))
        todos = cur.fetchall()

        if not todos:
            logger.info("user does not have todos")
            return Response("You have no todos yet.", 200)

        logger.debug(f"{len(todos)} todos found for {user.username} ")
        for todo in todos:
            todo_id, title, description, todo_type = todo
            print(f"ID: {todo_id} | Title: {title} | Description: {description or '-'} | Type: {todo_type}")

        return Response("Todos successfully retrieved.", 200)
    except Exception:
        logger.exception("somethong went wrong in server")
        return Response("Internal server error", 500)
