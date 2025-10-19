import bcrypt  #type:ignore



def hash_password(raw_password : str):
    encoded_password = raw_password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_password,salt).decode()



def match_password(raw_passowrd : str, encoded_password:str):
    raw_passowrd = raw_passowrd.encode()
    return bcrypt.checkpw(raw_passowrd,encoded_password.encode())





class Response:
    def __init__(self,message,status_code = 200):
        self.message = message
        self.status_code = status_code
        
    def __str__(self):
        return f'{self.message} =  {self.status_code}'