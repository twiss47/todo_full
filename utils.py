import bcrypt  #type:ignore
from serializers import UserRegister
import bcrypt
from serializers import UserRegister
from logger_config import logger

# Logger setup

def hash_password(raw_password: str):
    try:
        encoded_password = raw_password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(encoded_password, salt).decode()
        logger.debug("Password hashed successfully")
        return hashed
    except Exception:
        logger.exception("Error while hashing password")


def match_password(raw_password: str, encoded_password: str):
    try:
        raw_password = raw_password.encode()
        result = bcrypt.checkpw(raw_password, encoded_password.encode())
        logger.debug("Password matched" if result else "Password did not match")
        return result
    except Exception:
        logger.exception("Error while checking password match")


class Response:
    def __init__(self, message, status_code=200):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"{self.message} = {self.status_code}"


def login_required(func):
    def wrapper(*args, **kwargs):
        from session import Session
        session = Session()

        if session and session.session:
            logger.debug("User is logged in")
            return func(*args, **kwargs)
        else:
            logger.warning("Access denied: login required")
            return Response("Login required", 401)

    return wrapper


def validate_user(dto: UserRegister):
    try:
        assert dto.username, "Username must be required"
        assert dto.password, "Password must be required"
        logger.debug("User data validated successfully")
    except AssertionError as e:
        logger.error(f"Validation error: {e}")
        raise


def is_admin(func):
    def wrapper(*args, **kwargs):
        from session import Session
        session = Session()

        if not session.session:
            logger.warning("Access denied: login required")
            return Response('Login required', 401)
        
        if session.session.role != 'admin':
            logger.warning(f"Access denied for user {session.session.username}: not admin")
            return Response('Only admin user can be changed', 403)
        
        logger.debug(f"Admin access granted for {session.session.username}")
        return func(*args, **kwargs)
    return wrapper
